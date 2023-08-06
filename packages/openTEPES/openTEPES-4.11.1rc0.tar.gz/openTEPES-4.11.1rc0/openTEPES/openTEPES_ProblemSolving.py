"""
Open Generation, Storage, and Transmission Operation and Expansion Planning Model with RES and ESS (openTEPES) - March 28, 2023
"""

import time
import os
import pandas as pd
import psutil
import logging
from   pyomo.opt             import SolverFactory, SolverStatus, TerminationCondition
from   pyomo.util.infeasible import log_infeasible_constraints
from   pyomo.environ         import Param, Suffix, Set, NonNegativeReals, UnitInterval

def ProblemSolving(DirName, CaseName, SolverName, OptModel, mTEPES, pIndLogConsole):
    print('Problem solving                        ****')
    _path = os.path.join(DirName, CaseName)
    StartTime = time.time()

    #%% activating all periods, scenarios, and load levels
    mTEPES.del_component(mTEPES.st)
    mTEPES.del_component(mTEPES.n )
    mTEPES.st = Set(initialize=mTEPES.stt, ordered=True, doc='stages',      filter=lambda mTEPES,stt: stt in mTEPES.stt and mTEPES.pStageWeight[stt] and sum(1 for (stt,nn) in mTEPES.s2n))
    mTEPES.n  = Set(initialize=mTEPES.nn,  ordered=True, doc='load levels', filter=lambda mTEPES,nn : nn  in                mTEPES.pDuration                                              )

    #%% solving the problem
    Solver = SolverFactory(SolverName)                                                       # select solver
    if SolverName == 'gurobi':
        Solver.options['LogFile'       ] = _path+'/openTEPES_'+CaseName+'.log'
        # Solver.options['IISFile'     ] = _path+'/openTEPES_'+CaseName+'.ilp'               # should be uncommented to show results of IIS
        Solver.options['Method'        ] = 2                                                 # barrier method
        Solver.options['MIPFocus'      ] = 1
        Solver.options['Presolve'      ] = 2
        Solver.options['RINS'          ] = 100
        Solver.options['Crossover'     ] = -1
        # Solver.options['BarConvTol'    ] = 1e-9
        # Solver.options['BarQCPConvTol' ] = 0.025
        Solver.options['MIPGap'        ] = 0.01
        Solver.options['Threads'       ] = int((psutil.cpu_count(logical=True) + psutil.cpu_count(logical=False))/2)
        Solver.options['TimeLimit'     ] =    36000
        Solver.options['IterationLimit'] = 36000000
    if ( mTEPES.pIndBinGenInvest()*len(mTEPES.gc)*sum(mTEPES.pIndBinUnitInvest[gc] for gc in mTEPES.gc) + mTEPES.pIndBinGenRetire() *len(mTEPES.gd)*sum(mTEPES.pIndBinUnitRetire[gd] for gd in mTEPES.gd) + mTEPES.pIndBinNetInvest() *len(mTEPES.lc)*sum(mTEPES.pIndBinLineInvest[lc] for lc in mTEPES.lc) +
         mTEPES.pIndBinGenOperat()*len(mTEPES.nr)*sum(mTEPES.pIndBinUnitCommit[nr] for nr in mTEPES.nr) +                                                                                                   mTEPES.pIndBinLineCommit()*len(mTEPES.la)*sum(mTEPES.pIndBinLineSwitch[la] for la in mTEPES.la) + len(mTEPES.g2g) == 0 or
       (len(mTEPES.gc) == 0 or (len(mTEPES.gc) > 0 and mTEPES.pIndBinGenInvest() == 2)) and (len(mTEPES.gd) == 0 or (len(mTEPES.gd) > 0 and mTEPES.pIndBinGenRetire() == 2)) and (len(mTEPES.lc) == 0 or (len(mTEPES.lc) > 0 and mTEPES.pIndBinNetInvest() == 2))):
        # there are no binary decisions (no investment/retirement decisions or investment/retirement decisions already ignored, no line switching/unit commitment, no mutually exclusive units)
        OptModel.dual = Suffix(direction=Suffix.IMPORT)
        OptModel.rc   = Suffix(direction=Suffix.IMPORT)
    if (len(mTEPES.gc) == 0 or (len(mTEPES.gc) > 0 and mTEPES.pIndBinGenInvest() == 2)) and (len(mTEPES.gd) == 0 or (len(mTEPES.gd) > 0 and mTEPES.pIndBinGenRetire() == 2)) and (len(mTEPES.lc) == 0 or (len(mTEPES.lc) > 0 and mTEPES.pIndBinNetInvest() == 2)):
        # there are no expansion decisions, or they are ignored (it is an operation model)
        mTEPES.pScenProb_Saved   = Param(mTEPES.psc, initialize=mTEPES.pScenProb.extract_values()  , within=UnitInterval    , doc='Probability'       )
        mTEPES.pPeriodProb_Saved = Param(mTEPES.psc, initialize=mTEPES.pPeriodProb.extract_values(), within=NonNegativeReals, doc='Period probability')
        pScenProb = pd.Series([0.0 for p,sc in mTEPES.ps], index=mTEPES.ps)
        for p,sc in mTEPES.ps:
            if  mTEPES.pPeriodProb_Saved[p,sc] > 0.0:
                pScenProb[p,sc] = 1.0
                mTEPES.del_component(mTEPES.sc         )
                mTEPES.del_component(mTEPES.ps         )
                mTEPES.del_component(mTEPES.pPeriodProb)
                mTEPES.sc = Set(initialize=mTEPES.scc,         ordered=True, doc='scenarios'        , filter=lambda mTEPES,scc : scc    in mTEPES.scc         and pScenProb[p,sc] > 0.0)
                mTEPES.ps = Set(initialize=mTEPES.p*mTEPES.sc, ordered=True, doc='periods/scenarios', filter=lambda mTEPES,p,sc: (p,sc) in mTEPES.p*mTEPES.sc and pScenProb[p,sc] > 0.0)
                mTEPES.pPeriodProb = Param(mTEPES.ps, initialize=0.0, within=NonNegativeReals, doc='Period probability', mutable=True)
                mTEPES.pPeriodProb[p,sc] = mTEPES.pPeriodWeight[p]
                SolverResults = Solver.solve(OptModel, tee=True, report_timing=True)              # tee=True displays the log of the solver
                pScenProb[p,sc] = 0.0
        pScenProb = pd.Series([1.0 for p,sc in mTEPES.psc], index=mTEPES.psc)
        mTEPES.del_component(mTEPES.sc         )
        mTEPES.del_component(mTEPES.ps         )
        mTEPES.del_component(mTEPES.pPeriodProb)
        mTEPES.sc = Set(initialize=mTEPES.scc,         ordered=True, doc='scenarios'        , filter=lambda mTEPES,scc : scc    in mTEPES.scc         and pScenProb[p,sc] > 0.0)
        mTEPES.ps = Set(initialize=mTEPES.p*mTEPES.sc, ordered=True, doc='periods/scenarios', filter=lambda mTEPES,p,sc: (p,sc) in mTEPES.p*mTEPES.sc and pScenProb[p,sc] > 0.0)
        mTEPES.pScenProb   = Param(mTEPES.ps, initialize=1.0, within=UnitInterval,     doc='Probability',        mutable=True)
        mTEPES.pPeriodProb = Param(mTEPES.ps, initialize=0.0, within=NonNegativeReals, doc='Period probability', mutable=True)
        for p, sc in mTEPES.ps:
            mTEPES.pPeriodProb[p,sc] = mTEPES.pPeriodWeight[p] * mTEPES.pScenProb[p,sc]
    else:
        # there are investment decisions (it is an expansion and operation model)
        SolverResults = Solver.solve(OptModel, tee=True, report_timing=True)  # tee=True displays the log of the solver
    print('Termination condition: ', SolverResults.solver.termination_condition)
    if SolverResults.solver.termination_condition == TerminationCondition.infeasible:
        log_infeasible_constraints(OptModel, log_expression=True, log_variables=True)
        logging.basicConfig(filename=_path+'/openTEPES_Infeasibilities_'+CaseName+'.txt', level=logging.INFO)
    assert (SolverResults.solver.termination_condition == TerminationCondition.optimal or SolverResults.solver.termination_condition == TerminationCondition.maxTimeLimit or SolverResults.solver.termination_condition == TerminationCondition.infeasible.maxIterations), 'Problem infeasible'
    SolverResults.write()                                                              # summary of the solver results

    #%% fix values of some variables to get duals and solve it again
    # binary/continuous investment decisions are fixed to their optimal values
    # binary            operation  decisions are fixed to their optimal values
    if    (mTEPES.pIndBinGenInvest()*len(mTEPES.gc)*sum(mTEPES.pIndBinUnitInvest[gc] for gc in mTEPES.gc) + mTEPES.pIndBinGenRetire()*len(mTEPES.gd)*sum(mTEPES.pIndBinUnitRetire[gd] for gd in mTEPES.gd) + mTEPES.pIndBinNetInvest() *len(mTEPES.lc)*sum(mTEPES.pIndBinLineInvest[lc] for lc in mTEPES.lc) +
           mTEPES.pIndBinGenOperat()*len(mTEPES.nr)*sum(mTEPES.pIndBinUnitCommit[nr] for nr in mTEPES.nr) +                                                                                                  mTEPES.pIndBinLineCommit()*len(mTEPES.la)*sum(mTEPES.pIndBinLineSwitch[la] for la in mTEPES.la) + len(mTEPES.g2g) > 0 and
         ((len(mTEPES.gc) > 0 and mTEPES.pIndBinGenInvest() != 2) or (len(mTEPES.gd) > 0 and mTEPES.pIndBinGenRetire() != 2) or (len(mTEPES.lc) > 0 and mTEPES.pIndBinNetInvest() != 2))):
        if mTEPES.pIndBinGenInvest()*len(mTEPES.gc)*sum(mTEPES.pIndBinUnitInvest[gc] for gc in mTEPES.gc):
            for p,gc in mTEPES.pgc:
                if mTEPES.pIndBinUnitInvest[gc] != 0:
                    OptModel.vGenerationInvest[p,gc].fix(round(OptModel.vGenerationInvest[p,gc]()))
                else:
                    OptModel.vGenerationInvest[p,gc].fix(      OptModel.vGenerationInvest[p,gc]())
        if mTEPES.pIndBinGenRetire()*len(mTEPES.gd)*sum(mTEPES.pIndBinUnitRetire[gd] for gd in mTEPES.gd):
            for p,gd in mTEPES.pgd:
                if mTEPES.pIndBinUnitRetire[gd] != 0:
                    OptModel.vGenerationRetire[p,gd].fix(round(OptModel.vGenerationRetire[p,gd]()))
                else:
                    OptModel.vGenerationRetire[p,gd].fix(      OptModel.vGenerationRetire[p,gd]())
        if mTEPES.pIndBinNetInvest()*len(mTEPES.lc)*sum(mTEPES.pIndBinLineInvest[lc] for lc in mTEPES.lc):
            for p,ni,nf,cc in mTEPES.plc:
                if mTEPES.pIndBinLineInvest[ni,nf,cc] != 0:
                    OptModel.vNetworkInvest[p,ni,nf,cc].fix(round(OptModel.vNetworkInvest[p,ni,nf,cc]()))
                else:
                    OptModel.vNetworkInvest[p,ni,nf,cc].fix(      OptModel.vNetworkInvest[p,ni,nf,cc]())
        if mTEPES.pIndBinGenOperat()*len(mTEPES.nr)*sum(mTEPES.pIndBinUnitCommit[nr] for nr in mTEPES.nr):
            for p,sc,n,nr in mTEPES.psnnr:
                if mTEPES.pIndBinUnitCommit[nr] != 0:
                    OptModel.vCommitment[p,sc,n,nr].fix(round(OptModel.vCommitment[p,sc,n,nr]()))
                    OptModel.vStartUp   [p,sc,n,nr].fix(round(OptModel.vStartUp   [p,sc,n,nr]()))
                    OptModel.vShutDown  [p,sc,n,nr].fix(round(OptModel.vShutDown  [p,sc,n,nr]()))
        if mTEPES.pIndBinLineCommit()*len(mTEPES.la)*sum(mTEPES.pIndBinLineSwitch[la] for la in mTEPES.la):
            for p,sc,n,ni,nf,cc in mTEPES.psnla:
                if mTEPES.pIndBinLineSwitch[ni,nf,cc] != 0:
                    OptModel.vLineCommit  [p,sc,n,ni,nf,cc].fix(round(OptModel.vLineCommit   [p,sc,n,ni,nf,cc]()))
                    OptModel.vLineOnState [p,sc,n,ni,nf,cc].fix(round(OptModel.vLineOnState  [p,sc,n,ni,nf,cc]()))
                    OptModel.vLineOffState[p,sc,n,ni,nf,cc].fix(round(OptModel.vLineOffState [p,sc,n,ni,nf,cc]()))
                elif (ni,nf,cc) in mTEPES.lc:
                    OptModel.vLineCommit  [p,sc,n,ni,nf,cc].fix(round(OptModel.vNetworkInvest[p,     ni,nf,cc]()))
        if len(mTEPES.g2g):
            for nr in mTEPES.nr:
                if sum(1 for g in mTEPES.nr if (nr,g) in mTEPES.g2g or (g,nr) in mTEPES.g2g):
                    OptModel.vMaxCommitment[nr].fix(round(OptModel.vMaxCommitment[nr]()))
        OptModel.dual = Suffix(direction=Suffix.IMPORT)
        OptModel.rc   = Suffix(direction=Suffix.IMPORT)
        # there are no expansion decisions, or they are fixed (it is an operation model)
        pScenProb = pd.Series([0.0 for p,sc in mTEPES.ps], index=mTEPES.ps)
        for p,sc in mTEPES.ps:
            if  mTEPES.pPeriodProb_Saved[p,sc] > 0.0:
                pScenProb[p,sc] = 1.0
                mTEPES.del_component(mTEPES.sc         )
                mTEPES.del_component(mTEPES.ps         )
                mTEPES.del_component(mTEPES.pPeriodProb)
                mTEPES.sc = Set(initialize=mTEPES.scc,         ordered=True, doc='scenarios'        , filter=lambda mTEPES,scc : scc    in mTEPES.scc         and pScenProb[p,sc] > 0.0)
                mTEPES.ps = Set(initialize=mTEPES.p*mTEPES.sc, ordered=True, doc='periods/scenarios', filter=lambda mTEPES,p,sc: (p,sc) in mTEPES.p*mTEPES.sc and pScenProb[p,sc] > 0.0)
                mTEPES.pPeriodProb = Param(mTEPES.ps, initialize=0.0, within=NonNegativeReals, doc='Period probability', mutable=True)
                mTEPES.pPeriodProb[p,sc] = mTEPES.pPeriodWeight[p]
                SolverResults = Solver.solve(OptModel, tee=True, report_timing=True)              # tee=True displays the log of the solver
                pScenProb[p,sc] = 0.0
        pScenProb = pd.Series([1.0 for p,sc in mTEPES.psc], index=mTEPES.psc)
        mTEPES.del_component(mTEPES.sc         )
        mTEPES.del_component(mTEPES.ps         )
        mTEPES.del_component(mTEPES.pPeriodProb)
        mTEPES.sc = Set(initialize=mTEPES.scc,         ordered=True, doc='scenarios'        , filter=lambda mTEPES,scc : scc    in mTEPES.scc         and pScenProb[p,sc] > 0.0)
        mTEPES.ps = Set(initialize=mTEPES.p*mTEPES.sc, ordered=True, doc='periods/scenarios', filter=lambda mTEPES,p,sc: (p,sc) in mTEPES.p*mTEPES.sc and pScenProb[p,sc] > 0.0)
        mTEPES.pScenProb   = Param(mTEPES.ps, initialize=1.0, within=UnitInterval,     doc='Probability',        mutable=True)
        mTEPES.pPeriodProb = Param(mTEPES.ps, initialize=0.0, within=NonNegativeReals, doc='Period probability', mutable=True)
        for p, sc in mTEPES.ps:
            mTEPES.pPeriodProb[p,sc] = mTEPES.pPeriodWeight[p] * mTEPES.pScenProb[p,sc]

    SolvingTime = time.time() - StartTime
    print('Solution time                          ... ', round(SolvingTime), 's')
    print('Total system                   cost [MEUR] ', OptModel.eTotalSCost.expr())
    for p,sc in mTEPES.ps:
        print('***** Period: '+str(p)+', Scenario: '+str(sc)+' ******')
        print('  Total generation  investment cost [MEUR] ', sum(mTEPES.pDiscountFactor[p] * mTEPES.pGenInvestCost[gc      ]   * OptModel.vGenerationInvest[p,gc      ]() for gc       in mTEPES.gc))
        print('  Total generation  retirement cost [MEUR] ', sum(mTEPES.pDiscountFactor[p] * mTEPES.pGenRetireCost[gd      ]   * OptModel.vGenerationRetire[p,gd      ]() for gd       in mTEPES.gd))
        print('  Total network     investment cost [MEUR] ', sum(mTEPES.pDiscountFactor[p] * mTEPES.pNetFixedCost [ni,nf,cc]   * OptModel.vNetworkInvest   [p,ni,nf,cc]() for ni,nf,cc in mTEPES.lc))
        print('  Total generation  operation  cost [MEUR] ', sum(mTEPES.pDiscountFactor[p] * mTEPES.pScenProb     [p,sc    ]() * OptModel.vTotalGCost      [p,sc,n    ]() for n        in mTEPES.n ))
        print('  Total consumption operation  cost [MEUR] ', sum(mTEPES.pDiscountFactor[p] * mTEPES.pScenProb     [p,sc    ]() * OptModel.vTotalCCost      [p,sc,n    ]() for n        in mTEPES.n ))
        print('  Total emission               cost [MEUR] ', sum(mTEPES.pDiscountFactor[p] * mTEPES.pScenProb     [p,sc    ]() * OptModel.vTotalECost      [p,sc,n    ]() for n        in mTEPES.n ))
        print('  Total reliability            cost [MEUR] ', sum(mTEPES.pDiscountFactor[p] * mTEPES.pScenProb     [p,sc    ]() * OptModel.vTotalRCost      [p,sc,n    ]() for n        in mTEPES.n ))
