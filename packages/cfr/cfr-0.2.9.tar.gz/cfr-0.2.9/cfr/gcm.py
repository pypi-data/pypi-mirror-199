import os
import glob
import xarray as xr
import numpy as np
from tqdm import tqdm
from . import visual
from .climate import ClimateField
from .utils import (
    coefficient_efficiency,
    p_header,
    p_hint,
    p_success,
    p_fail,
    p_warning,
)

class CESMarchive:
    ''' The class for postprocessing the CESM archives
    
    Args:
        dirpath (str): the directory path where the reconstruction results are stored.
        load_num (int): the number of ensembles to load
        verbose (bool, optional): print verbose information. Defaults to False.
    '''

    def __init__(self, dirpath, load_num=None, tag='h', exclude_tags=['nday', 'once'], verbose=False):
        if type(exclude_tags) is str:
            exclude_tags = [exclude_tags]

        try:
            fpaths = sorted(glob.glob(os.path.join(dirpath, f'*{tag}*.nc')))
            if load_num is not None:
                fpaths = fpaths[:load_num]
            
            self.paths = []
            for path in fpaths:
                include = True
                for ex_tag in exclude_tags:
                    if ex_tag in path:
                        include = False

                if include:
                    self.paths.append(path)
        except:
            raise ValueError('No CESM archive files available at `dirpath`!')

        if verbose:
            p_header(f'>>> {len(self.paths)} CESMarchive.paths:')
            print(self.paths)

        self.fd = {}

    def get_ds(self, fid=0):
        ''' Get a `xarray.Dataset` from a certain file
        '''
        with xr.open_dataset(self.paths[fid]) as ds:
            return ds

    def load(self, vn_list, time_name='time', verbose=False):
        ''' Load variables.

        Args:
            vn_list (list): list of variable names
            verbose (bool, optional): print verbose information. Defaults to False.
        '''
        if type(vn_list) is str:
            vn_list = [vn_list]

        ds_list = []
        for path in tqdm(self.paths, desc='Loading files'):
            with xr.open_dataset(path) as ds_tmp:
                ds_list.append(ds_tmp)

        for vn in vn_list:
            p_header(f'Extracting {vn} ...')
            da = xr.concat([ds[vn] for ds in ds_list], dim=time_name)
            self.fd[vn] = ClimateField().from_da(da)

            if verbose:
                p_success(f'>>> CESMarchive.fd["{vn}"] created')