from collections import OrderedDict
from collections import namedtuple
import os
import copy
import mne
import numpy as np
import pandas as pd
import statsmodels.api as sm
import pingouin as pg
import matplotlib.pyplot as plt
import scipy


def input_condition_ecodes():
    print('Enter condition event codes:')
    conditions = input().split(' ')
    for i in range(len(conditions)): conditions[i] = int(conditions[i])
    return conditions

def input_unique_codes():
    print('Enter List 1 unique codes xlsx file:')
    uc1_xlsx = input()
    print('Enter List 2 unique codes xlsx file:')
    uc2_xlsx = input()
    return (uc1_xlsx, uc2_xlsx)

def input_predictors():
    print('Enter List 1 predictors xlsx file:')
    pred1 = input()
    print('Enter List 2 predictors xlsx file:')
    pred2 = input()
    return (pred1, pred2)
    

class subject:
    def __init__(self, list_num, eeglab_elist, mne_raw):
        self.list_num = list_num
        self.eeglab_elist = eeglab_elist
        self.mne_raw = mne_raw

        
    def load_unique_codes(self ,uc1_xlsx, uc2_xlsx):
        if self.list_num == 1: return pd.read_excel(uc1_xlsx).to_numpy()
        elif self.list_num == 2: return pd.read_excel(uc2_xlsx).to_numpy()
        else: return None       

        
    def load_predictors(self, pred1_xlsx, pred2_xlsx, drop_col=[]):
        if self.list_num == 1:
            df = pd.read_excel(pred1_xlsx)
            intercept = np.ones((len(df.index)))
            if drop_col != []: df = df.drop(df.columns[drop_col], axis=1)
            df.insert(0, 'intercept', intercept)
            return df.to_numpy()
      
        elif self.list_num == 2:
            df = pd.read_excel(pred2_xlsx)
            intercept = np.ones((len(df.index)))
            if drop_col != []: df = df.drop(df.columns[drop_col], axis=1)
            df.insert(0, 'intercept', intercept)
            return df.to_numpy()
      
        else: return None
        
        
    def split_elist(self):
        open_txt = open(self.eeglab_elist, 'r')
        read_txt = open_txt.readlines()
        open_txt.close
        
        split_txt = []
        for i in read_txt:
            split_txt.append(i.split())
        return split_txt
        
        
    def check_elist(self, condition_ecodes, unique_codes):   
        prefinal_codes = []
        for i in range(len(self.split_elist())):
            if int(self.split_elist()[i][2]) in condition_ecodes:
                prefinal_codes.append(int(self.split_elist()[i-1][2]))
                
        check = False
        if len(prefinal_codes) == len(unique_codes):
            for i in range(len(unique_codes)):
                 if prefinal_codes[i] != unique_codes[i]:
                        check = True
                        return prefinal_codes
                        break
            if check == False:
                print('\nNo mismatch found :D\n')
                return None
        else: 
            return prefinal_codes
        
            
    def drop_marked_epochs(self, predictors, condition_ecodes, col=[]):
        ep_all = []
        for i in self.split_elist():
            if int(i[2]) in condition_ecodes: ep_all.append([i[2], i[8]])
                
        ep_unmarked = []
        dm = np.zeros((0, np.shape(predictors)[1]))
        for i in range(len(ep_all)):
            if int(ep_all[i][1]) == 0:
                ep_unmarked.append(ep_all[i][0])
                dm = np.r_[dm, [predictors[i]]]
        Unmarked = namedtuple('Unmarked', ['Epoch_Ecodes', 'Dmatrix'])
        unmarked = Unmarked(ep_unmarked, dm)
        return unmarked
    
    
    def sort_predictors(self, unique_codes, predictors, condition_ecodes, col=[]):
        ep_all = []
        for i in self.split_elist():
            if int(i[2]) in condition_ecodes: ep_all.append([i[2], i[8]])
                
        dm = np.zeros((0, np.shape(predictors)[1]))
        prefinal_codes = self.check_elist(condition_ecodes, unique_codes)
        index = None
        for i in range(len(unique_codes)):
            if unique_codes[i] == prefinal_codes[0]:
                index = i
                break
        predictors = np.concatenate((predictors[index:], predictors[0:index]), axis=0)
        for i in range(len(ep_all)):
            if int(ep_all[i][1]) == 0:
                dm = np.r_[dm, [predictors[i]]] 
        return dm
    

    def create_chan_dict(self):
        ch_list = self.mne_raw.ch_names
        ch_dict = OrderedDict()
        for i in range(len(ch_list)):
            ch_dict.update({ch_list[i]: i})
        return ch_dict
          
    
    def get_events(self):
        events_from_annot = mne.events_from_annotations(self.mne_raw, event_id='auto')
        EventsInfo = namedtuple('EventsInfo', ['Events', 'Events_Dict'])
        eventsinfo = EventsInfo(events_from_annot[0], events_from_annot[1])   
        return eventsinfo
    
    
    def AD_compiler(self, condition_ecodes):          
        marked_item_nums = [] # a list of the a-flagged item numbers
        for i in range(len(self.split_elist())):
            if int(self.split_elist()[i][2]) in condition_ecodes and int(self.split_elist()[i][8]) != 0:
                marked_item_nums.append(i)
        
        annot = self.mne_raw.annotations
        onsets = np.empty((len(annot)))
        durations = np.empty((len(annot)))
        descriptions = []
        for i in range(len(annot)):
            onsets[i] = copy.deepcopy(annot[i])['onset']
            durations[i] = copy.deepcopy(annot[i])['duration']
            descriptions.append(copy.deepcopy(annot[i])['description'])
            
        for i in marked_item_nums:
            descriptions[i] = 'bad_blink'
        
        new_annot = mne.Annotations(onsets, durations, np.array(descriptions), orig_time=None, ch_names=None)
        return new_annot
    
    
def rerp_ols(mne_epoch, X, pred_names=None):
    if pred_names == None:
        pred_names = []
        for i in range(np.shape(X)[1]):
            pred_names.append('x'+str(i))
            
    rERP_OLS_Wrapper = namedtuple('rERP_OLS_Wrapper', ['Coeffs', 'Fitted', 'Resids'])
    Coeffs_Info = namedtuple('Coeffs_Info', ['beta', 'tval', 'pval'])
    
    X_t = np.transpose(X)
    XX_t = np.matmul(X_t, X)
    inv_XX_t = np.linalg.inv(XX_t)
    
    data = mne_epoch.copy().get_data()
    num_ep = np.shape(data)[0]
    num_ch = np.shape(data)[1]
    num_t = np.shape(data)[2]
    
    coeffs = np.empty((np.shape(X)[1], num_ch, num_t))
    fitted = np.empty((num_ep, num_ch, num_t))
    resids = np.empty((num_ep, num_ch, num_t))
    
    for ch in range(num_ch):
        Y = data[:,ch,:]
        sol = np.matmul(inv_XX_t, X_t)
        coeffs[:,ch,:] = np.matmul(sol, Y)
        fitted[:,ch,:] = np.matmul(X, coeffs[:,ch,:])
        resids[:,ch,:] = np.subtract(Y, fitted[:,ch,:])
    
    beta_arr = np.empty((np.shape(X)[1], num_ch, num_t))
    tval_arr = np.empty((np.shape(X)[1], num_ch, num_t))
    pval_arr = np.empty((np.shape(X)[1], num_ch, num_t))
    
    rerp = mne.stats.linear_regression(mne_epoch, X, names=pred_names)
    for i in range(len(pred_names)):
        beta_arr[i] = rerp[pred_names[i]].beta.data
        tval_arr[i] = rerp[pred_names[i]].t_val.data
        pval_arr[i] = rerp[pred_names[i]].p_val.data
        
    coeffs_dict = {'coeffs_arr': coeffs}
    for i in range(len(pred_names)):
        coeffs_dict[pred_names[i]] = Coeffs_Info(beta_arr[i], tval_arr[i], pval_arr[i])
        
    rerp_ols_wrapper = rERP_OLS_Wrapper(coeffs_dict, fitted, resids)
    return rerp_ols_wrapper


class rERP:
    def __init__(self, mne_epoch, epoch_ecodes, condition_ecodes):
        self.mne_epoch = mne_epoch
        self.epoch_ecodes = epoch_ecodes
        self.condition_ecodes = condition_ecodes
    
    
    def bins_dummy_code(self):
        dmatrix = np.zeros((len(self.epoch_ecodes), len(self.condition_ecodes)))
        for i in range(len(self.condition_ecodes)):
            for j in range((len(self.epoch_ecodes))):
                if int(self.epoch_ecodes[j]) == self.condition_ecodes[i]:
                    dmatrix[j][i] = 1
        return dmatrix
    
    
    def linear_regression(self, dmatrix, names_list):
        res = rerp_ols(self.mne_epoch, dmatrix, pred_names=names_list)
        return res
            
    
    def compute_condition_means(self, res):
        data_arr = self.mne_epoch.copy().get_data()
        num_ch = np.shape(data_arr)[1]
        num_t = np.shape(data_arr)[2]
        
        mean_fitted = np.zeros((len(self.condition_ecodes), num_ch, num_t))
        mean_resids = np.zeros((len(self.condition_ecodes), num_ch, num_t))
        count = np.zeros((len(self.condition_ecodes)))
        
        for i in range(len(self.condition_ecodes)):
            for j in range((len(self.epoch_ecodes))):
                if int(self.epoch_ecodes[j]) == self.condition_ecodes[i]:
                    mean_fitted[i] = np.add(mean_fitted[i], res.Fitted[j])
                    mean_resids[i] = np.add(mean_fitted[i], res.Resids[j])
                    count[i] += 1
        
        for i in range(len(self.condition_ecodes)):
            mean_fitted[i] = np.multiply(mean_fitted[i], 1/count[i])
            mean_resids[i] = np.multiply(mean_resids[i], 1/count[i])
        
        Condition_Means = namedtuple('Condition_Means', ['Mean_Fitted', 'Mean_Resids'])
        condition_means = Condition_Means(mean_fitted, mean_resids)
        return condition_means

def muV(arr):
    arr = np.multiply(arr, 10**6)
    return arr


rERP_Outputs = namedtuple('rERP_Outputs', ['Regr_Res', 'Cond_Means'])
Regr_Res = namedtuple('Regr_Res', ['Bins', 'rERP'])
Cond_Means = namedtuple('Cond_Means', ['Bins', 'rERP'])
Component_Means = namedtuple('Component_Means', ['Bins', 'rERP'])

class iteration(subject):
    def __init__(self, list_num, eeglab_elist, mne_raw, condition_ecodes, uc, pred, col_todrop=[]):
        super().__init__(list_num, eeglab_elist, mne_raw)
        self.col_todrop = col_todrop
        self.unique_codes = self.load_unique_codes(uc[0], uc[1])
        self.predictors = self.load_predictors(pred[0], pred[1], drop_col=col_todrop)
        self.condition_ecodes = condition_ecodes
        self.chan_dict = self.create_chan_dict()
        
        
    def get_rerp_outputs(self):
        predictors = self.predictors
        condition_ecodes = self.condition_ecodes
        unique_codes = self.unique_codes
        ecodes = self.drop_marked_epochs(predictors, condition_ecodes, col=self.col_todrop).Epoch_Ecodes
            
        ev = self.get_events().Events
        ev_dict = self.get_events().Events_Dict
        all_ev = []
        c = min([eval(i) for i in ecodes])
        for i in range(max([eval(i) for i in ecodes]) - min([eval(i) for i in ecodes]) + 1):
            all_ev.append(ev_dict[str(c+i)])
                
        self.mne_raw.set_annotations(self.AD_compiler(condition_ecodes))
        all_epoched_bc = mne.Epochs(self.mne_raw, ev, event_id=all_ev, tmin=-0.1, tmax=1.0, baseline=(-0.1,0.0),
                                    reject_by_annotation=True)
        
        if self.check_elist(condition_ecodes, unique_codes) == None:
            X = self.drop_marked_epochs(predictors, condition_ecodes, col=self.col_todrop).Dmatrix
            
        else: 
            print('\nError: Unique codes do not match !!! Sorting...\n')
            X = self.sort_predictors(unique_codes, predictors, condition_ecodes, col=self.col_todrop)
            
        all_trials = rERP(all_epoched_bc, ecodes, condition_ecodes)
          
        X_bins = all_trials.bins_dummy_code()
          
        res_bins = all_trials.linear_regression(X_bins, None)     
        res_rerp = all_trials.linear_regression(X, None)  
        
        cond_means_bins = all_trials.compute_condition_means(res_bins)
        cond_means_rerp = all_trials.compute_condition_means(res_rerp)  
        
        regr_res = Regr_Res(res_bins, res_rerp)
        cond_means = Cond_Means(cond_means_bins, cond_means_rerp)
        rerp_outputs = rERP_Outputs(regr_res, cond_means) 
        return rerp_outputs
        
    
    def get_component_means(self, rerp_outputs, timewindow, ch_names_list):
        outputs = np.array([rerp_outputs.Cond_Means.Bins.Mean_Fitted,          # shape(num_coeffs, 35, 1101)
                            rerp_outputs.Cond_Means.rERP.Mean_Fitted],         # shape(num_coeffs, 35, 1101)
                            dtype=object)
        
        means = np.array([np.zeros((np.shape(outputs[0])[0], np.shape(outputs[0])[1])),    # shape(num_coeffs, 35)
                          np.zeros((np.shape(outputs[1])[0], np.shape(outputs[1])[1]))],   # shape(num_coeffs, 35)
                          dtype=object)
        
        for i in range(np.shape(means)[0]):
            for t in range(max(timewindow) - min(timewindow) + 1):
                means[i] = np.add(means[i], outputs[i][:,:,min(timewindow) + 100 + t])
        means = np.multiply(means, 1/(max(timewindow) - min(timewindow) + 1))
        
        ch_idx = []
        for ch in ch_names_list: ch_idx.append(self.chan_dict[ch])
        
        ch_means = np.array([np.zeros((np.shape(outputs[0])[0])),
                             np.zeros((np.shape(outputs[1])[0]))], dtype=object)
                
        for i in range(np.shape(ch_means)[0]):
            for j in ch_idx:
                ch_means[i] = np.add(ch_means[i], means[i][:,j])
        ch_means = np.multiply(ch_means, 1/len(ch_idx))
        
        component_means = Component_Means(ch_means[0], ch_means[1])
        return component_means  
    
    
    def get_coeffs_means(self, rerp_outputs, timewindow, ch_names_list):
        outputs = rerp_outputs.Regr_Res.rERP.Coeffs['coeffs_arr']       # shape(8, 35, 1101) 
        
        means = np.zeros((np.shape(outputs)[0], np.shape(outputs)[1]))  # shape(8, 35)                  
        
        for t in range(max(timewindow) - min(timewindow) + 1):
            means = np.add(means, outputs[:,:,min(timewindow) + 100 + t])
        means = np.multiply(means, 1/(max(timewindow) - min(timewindow) + 1))
        
        ch_idx = []
        for ch in ch_names_list: ch_idx.append(self.chan_dict[ch])
        
        ch_means = np.zeros((np.shape(outputs)[0]))
        
        for j in ch_idx:
            ch_means = np.add(ch_means, means[:,j])
        ch_means = np.multiply(ch_means, 1/len(ch_idx))
        
        return ch_means

    
Grand_Averages = namedtuple('Grand_Averages', ['ERP_Bins', 'rERP_Effects', 'rERP_Estimates', 'Residuals'])

class grand:
    def __init__(self, subj_outputs):
        self.subj_outputs = subj_outputs
        
    def compute_grand_averages(self):
        num_bins = np.shape(self.subj_outputs[0].Regr_Res.Bins.Coeffs['coeffs_arr'])[0]
        num_pred = np.shape(self.subj_outputs[0].Regr_Res.rERP.Coeffs['coeffs_arr'])[0]
        num_ch = np.shape(self.subj_outputs[0].Regr_Res.rERP.Coeffs['coeffs_arr'])[1]
        num_t = np.shape(self.subj_outputs[0].Regr_Res.rERP.Coeffs['coeffs_arr'])[2]
        
        gnd_avgs = np.array([np.zeros((num_bins, num_ch, num_t)),
                             np.zeros((num_pred, num_ch, num_t)),
                             np.zeros((2, num_bins, num_ch, num_t))], dtype=object)
        rerp_coeffs = np.empty((num_pred, num_ch, num_t))
        rerp_cond_means = np.empty((2, num_bins, num_ch, num_t))
        for i in range(np.shape(self.subj_outputs)[0]):
            rerp_coeffs = self.subj_outputs[i].Regr_Res.rERP.Coeffs['coeffs_arr']
            rerp_cond_means = np.array([self.subj_outputs[i].Cond_Means.rERP.Mean_Fitted,
                                        self.subj_outputs[i].Cond_Means.rERP.Mean_Resids], dtype=object)
            
            gnd_avgs = np.add(gnd_avgs, np.array([self.subj_outputs[i].Regr_Res.Bins.Coeffs['coeffs_arr'],
                                                  rerp_coeffs, rerp_cond_means],
                              dtype=object), dtype=object)
            
        gnd_avgs = np.multiply(gnd_avgs, 1/np.shape(self.subj_outputs)[0])
        
        grand_averages = Grand_Averages(gnd_avgs[0], gnd_avgs[1], gnd_avgs[2][0], gnd_avgs[2][1])
        return grand_averages

    
class eeg_graphs:
    def __init__(self, chan_dict, timeline, grand_averages=None, single_subj_rerp_outputs=None):
        self.chan_dict = chan_dict
        self.timeline = timeline
        self.grand_averages = grand_averages
        self.single_subj_rerp_outputs = single_subj_rerp_outputs
        
    def plot_grand_average_rERP_effects(self, ch_names_arr, fig_size,
                                        effect_colors = ['black', 'darkorange', 'gold', 'red', 'brown']):
        labels = np.array(['Intercept', 'Fval', 'Wemo', 'Plaus', 'Fval*Wemo'])
        num_coeffs = np.shape(self.grand_averages.rERP_Effects)[0]
        if np.shape(ch_names_arr) == (1,1):
            ch = ch_names_arr[0][0]
            figure, axis = plt.subplots(figsize=fig_size)
            for i in range(num_coeffs-1):
                axis.plot(self.timeline, muV(self.grand_averages.rERP_Effects[i+1][self.chan_dict[ch]]),
                         color=effect_colors[i+1], label=labels[i+1])
            axis.axvline(x=0, color='black', linewidth=0.5)
            axis.axhline(y=0, color='black', linewidth=0.5)
            axis.set_title(ch)
            axis.invert_yaxis()
            hdl, lbl = axis.get_legend_handles_labels()
            figure.legend(hdl, lbl, loc='upper left', bbox_to_anchor=[-0.001, 0.001])
            figure.tight_layout()
            plt.show()                   
                
        else:
            figure, axis = plt.subplots(np.shape(ch_names_arr)[0], np.shape(ch_names_arr)[1], figsize=fig_size)
            for ax, ch in zip(axis.copy().flatten(), ch_names_arr.copy().flatten()):
                for i in range(num_coeffs-1):
                    ax.plot(self.timeline, muV(self.grand_averages.rERP_Effects[i+1][self.chan_dict[ch]]),
                            color=effect_colors[i+1], label=labels[i+1])
                ax.axvline(x=0, color='black', linewidth=0.5)
                ax.axhline(y=0, color='black', linewidth=0.5)
                ax.set_title(ch)
                ax.invert_yaxis()
            hdl, lbl = ax.get_legend_handles_labels()
            figure.legend(hdl, lbl, loc='upper left', bbox_to_anchor=[-0.001, 0.001])
            figure.tight_layout()
            plt.show()
            
    def plot_grand_average_ERPs(self, conditions, ch_names_arr, fig_size,
                                bins_colors = ['navy', 'royalblue', 'forestgreen', 'yellowgreen']):
        cond_dict = {'HEC': 0, 'HEI': 1, 'HNC': 2, 'HNI': 3, 'LEC': 4, 'LEI': 5, 'LNC': 6, 'LNI': 7}
        if np.shape(ch_names_arr) == (1,1):
            ch = ch_names_arr[0][0]
            figure, axis = plt.subplots(figsize=fig_size)
            for i in range(len(conditions)):
                axis.plot(self.timeline, muV(self.grand_averages.ERP_Bins[cond_dict[conditions[i]]][self.chan_dict[ch]]),
                        color=bins_colors[i], label=conditions[i])
            axis.axvline(x=0, color='black', linewidth=0.5)
            axis.axhline(y=0, color='black', linewidth=0.5)
            axis.set_title(ch)
            axis.invert_yaxis()
            hdl, lbl = axis.get_legend_handles_labels()
            figure.legend(hdl, lbl, loc='upper left', bbox_to_anchor=[-0.001, 0.001])
            figure.tight_layout()
            plt.show()
             
        else:
            figure, axis = plt.subplots(np.shape(ch_names_arr)[0], np.shape(ch_names_arr)[1], figsize=fig_size)
            for ax, ch in zip(axis.copy().flatten(), ch_names_arr.copy().flatten()):
                for i in range(len(conditions)):
                    ax.plot(self.timeline, muV(self.grand_averages.ERP_Bins[cond_dict[conditions[i]]][self.chan_dict[ch]]),
                            color=bins_colors[i], label=conditions[i])
                ax.axvline(x=0, color='black', linewidth=0.5)
                ax.axhline(y=0, color='black', linewidth=0.5)
                ax.set_title(ch)
                ax.invert_yaxis()
            hdl, lbl = ax.get_legend_handles_labels()
            figure.legend(hdl, lbl, loc='upper left', bbox_to_anchor=[-0.001, 0.001])
            figure.tight_layout()
            plt.show()
            
            
    def plot_grand_average_rERPs(self, conditions, ch_names_arr, fig_size,
                                 conditions_colors = ['navy', 'royalblue', 'forestgreen', 'yellowgreen']):
        cond_dict = {'HEC': 0, 'HEI': 1, 'HNC': 2, 'HNI': 3, 'LEC': 4, 'LEI': 5, 'LNC': 6, 'LNI': 7}
        if np.shape(ch_names_arr) == (1,1):
            ch = ch_names_arr[0][0]
            figure, axis = plt.subplots(figsize=fig_size)
            for i in range(len(conditions)):
                axis.plot(self.timeline, muV(self.grand_averages.rERP_Estimates[cond_dict[conditions[i]]][self.chan_dict[ch]]),
                        color=conditions_colors[i], label=conditions[i])
            axis.axvline(x=0, color='black', linewidth=0.5)
            axis.axhline(y=0, color='black', linewidth=0.5)
            axis.set_title(ch)
            axis.invert_yaxis()
            hdl, lbl = axis.get_legend_handles_labels()
            figure.legend(hdl, lbl, loc='upper left', bbox_to_anchor=[-0.001, 0.001])
            figure.tight_layout()
            plt.show()
             
        else:
            figure, axis = plt.subplots(np.shape(ch_names_arr)[0], np.shape(ch_names_arr)[1], figsize=fig_size)
            for ax, ch in zip(axis.copy().flatten(), ch_names_arr.copy().flatten()):
                for i in range(len(conditions)):
                    ax.plot(self.timeline, muV(self.grand_averages.rERP_Estimates[cond_dict[conditions[i]]][self.chan_dict[ch]]),
                            color=conditions_colors[i], label=conditions[i])
                ax.axvline(x=0, color='black', linewidth=0.5)
                ax.axhline(y=0, color='black', linewidth=0.5)
                ax.set_title(ch)
                ax.invert_yaxis()
            hdl, lbl = ax.get_legend_handles_labels()
            figure.legend(hdl, lbl, loc='upper left', bbox_to_anchor=[-0.001, 0.001])
            figure.tight_layout()
            plt.show()
