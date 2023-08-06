# -*- coding: utf-8 -*-
import copy, pdb
import numpy as np
import pandas as pd
from ultron.tradingday import *
from ultron.factor.covariance.cov_engine import CovEngine
from ultron.strategy.strategy import create_params

from ultron.optimize.riskmodel import FullRiskModel
from jdw.kdutils.logger import kd_logger
from jdw.mfc.entropy.gravity.dendall.base import Base
from jdw.data.SurfaceAPI.universe import FutUniverse
from jdw.data.SurfaceAPI.futures.yields import FutYields
from jdw.data.SurfaceAPI.index_market import IndexMarket
from jdw.data.SurfaceAPI.futures.classify import FutClassify


class FuturesDendall(Base):

    def __init__(self,
                 horizon=0,
                 offset=0,
                 cov_window=20,
                 cov_model='unshrunk',
                 industry_name='kh',
                 industry_level=1,
                 factors_data=None,
                 benchmark=None,
                 universe=None):
        super(FuturesDendall, self).__init__(industry_class=FutClassify,
                                             universe_class=FutUniverse,
                                             index_yields_class=IndexMarket,
                                             yields_class=FutYields,
                                             horizon=horizon,
                                             offset=offset,
                                             industry_name=industry_name,
                                             industry_level=industry_level,
                                             factors_data=factors_data,
                                             benchmark=benchmark,
                                             universe=universe)
        self._cov_window = cov_window
        self._cov_model = cov_model
        self._category = 'longshort'

    def merge(self, industry_data, component_data):
        industry_dummy = pd.get_dummies(
            industry_data.set_index(['trade_date',
                                     'code'])['industry_code']).reset_index()

        total_data = component_data.merge(
            industry_data.drop(['trade_date'], axis=1),
            on=['code']).merge(industry_dummy.drop(['trade_date'], axis=1),
                               on=['code'])
        return total_data

    def create_riskmodel(self, begin_date, end_date, universe=None):
        models = {}
        start_date = advanceDateByCalendar('china.sse', begin_date,
                                           "-{}b".format(self._cov_window),
                                           BizDayConventions.Following)
        yields_data = FutYields().fetch_yileds(universe=universe,
                                               start_date=start_date,
                                               end_date=end_date,
                                               name='ret')
        yields_data = yields_data.set_index(['trade_date', 'code']).unstack()
        #returns_data_groups = yields_data.groupby('trade_date')
        dates = makeSchedule(begin_date, end_date, '1b', calendar='china.sse')
        for ref_date in dates:
            ref_begin_date = advanceDateByCalendar(
                'china.sse', ref_date, '-{0}b'.format(self._cov_window))
            ref_end_date = advanceDateByCalendar('china.sse', ref_date, '-0b')
            rtb = yields_data.loc[ref_begin_date:ref_end_date].fillna(0)
            cov = CovEngine.calc_cov(name=self._cov_model,
                                     ret_tb=rtb,
                                     window=self._cov_window)
            model = FullRiskModel(cov)
            models[ref_date] = model
        return models, None, None

    def create_component(self, begin_date, end_date, universe=None):
        yields_data = FutYields().fetch_yileds(
            universe=FutUniverse(u_name=universe),
            start_date=begin_date,
            end_date=end_date,
            name='ret')
        factors = yields_data.set_index(['trade_date', 'code']).unstack()
        rank = factors.rank(axis=1, method='dense')
        score = (rank - 0.5).div(rank.max(axis=1), axis='rows') - 0.5
        right_weight = copy.deepcopy(score)
        right_weight[right_weight <= 0] = np.nan
        right_weight[right_weight <= 0] = np.nan
        right_weight = right_weight.div(right_weight.sum(axis=1, min_count=1),
                                        axis='rows')
        left_weight = copy.deepcopy(score)
        left_weight[left_weight >= 0] = np.nan
        left_weight = left_weight.div(left_weight.sum(axis=1, min_count=1),
                                      axis='rows')
        both_weight = right_weight.sub(left_weight, fill_value=0)
        both_weight = both_weight.stack()
        return both_weight.reset_index().rename(columns={'nxt1_ret': 'weight'})
