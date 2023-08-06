__author__ = "Simon Nilsson"

from simba.read_config_unit_tests import (check_if_dir_exists,
                                          check_if_filepath_list_is_empty)
from simba.mixins.config_reader import ConfigReader
import os, glob
from simba.rw_dfs import read_df, save_df
from simba.misc_tools import get_fn_ext
from simba.third_party_label_appenders_test.tools import additional_third_party_clf_test
from simba.utils.errors import (ThirdPartyAnnotationOverlapError,
                                ThirdPartyAnnotationEventCountError,
                                InvalidFileTypeError)
from simba.utils.warnings import (ThirdPartyAnnotationsOutsidePoseEstimationDataWarning,
                                  ThirdPartyAnnotationsInvalidFileFormatWarning,
                                  ThirdPartyAnnotationsAdditionalClfWarning)
import pandas as pd
from simba.enums import Methods, Dtypes
from copy import deepcopy

MEDIA_FILE_PATH = 'Media file path'
OBSERVATION_ID = 'Observation id'
TIME = 'Time'
FPS = 'FPS'
BEHAVIOR = 'Behavior'
STATUS = 'Status'
START = 'START'
STOP = 'STOP'

EXPECTED_HEADERS = [TIME, MEDIA_FILE_PATH, FPS, BEHAVIOR, STATUS]

class BorisAppender(ConfigReader):

    """
    Class for appending BORIS human annotations onto featurized pose-estimation data.

    Parameters
    ----------
    config_path: str
        path to SimBA project config file in Configparser format
    boris_folder: str
        path to folder holding BORIS data files is CSV format

    Notes
    ----------
    `Example BORIS input file <https://github.com/sgoldenlab/simba/blob/master/misc/boris_example.csv`__.

    Examples
    ----------
    >>> boris_appender = BorisAppender(config_path='MyProjectConfigPath', data_dir=r'BorisDataFolder')
    >>> boris_appender.create_boris_master_file()
    >>> boris_appender.run()

    References
    ----------

    .. [1] `Behavioral Observation Research Interactive Software (BORIS) user guide <https://boris.readthedocs.io/en/latest/#>`__.
    """

    def __init__(self,
                 config_path: str,
                 data_dir: str,
                 settings: dict):

        super().__init__(config_path=config_path)
        check_if_dir_exists(in_dir=data_dir)
        self.data_dir, self.settings = data_dir, settings
        self.error_settings = self.settings['errors']
        self.data_file_paths = glob.glob(self.data_dir + '/*.csv')
        check_if_filepath_list_is_empty(filepaths=self.data_file_paths,
                                        error_msg=f'SIMBA ERROR: ZERO BORIS CSV files found in {data_dir} directory')
        print(f'Processing BORIS for {str(len(self.feature_file_paths))} file(s)...')

    def create_boris_master_file(self):
        """
        Method to create concatenated dataframe of BORIS annotations CSV files in directory.
        """
        self.df_lst = []
        for file_cnt, file_path in enumerate(self.data_file_paths):
            _, video_name, _ = get_fn_ext(file_path)
            boris_df = pd.read_csv(file_path)
            try:
                start_idx = (boris_df[boris_df[OBSERVATION_ID] == TIME].index.values)
                df = pd.read_csv(file_path, skiprows=range(0, int(start_idx + 1)))[EXPECTED_HEADERS]
                _, video_base_name, _ = get_fn_ext(df.loc[0, MEDIA_FILE_PATH])
                df[MEDIA_FILE_PATH] = video_base_name
                self.df_lst.append(df)
            except Exception as e:
                print(e)
                if self.error_settings[Methods.INVALID_THIRD_PARTY_APPENDER_FILE.value] == Methods.WARNING.value:
                    ThirdPartyAnnotationsInvalidFileFormatWarning(annotation_app='BORIS', file_path=file_path)
                elif self.error_settings[Methods.INVALID_THIRD_PARTY_APPENDER_FILE.value] == Methods.ERROR.value:
                    raise InvalidFileTypeError(msg=f'{file_path} is not a valid BORIS file. See the docs for expected file format')
                else:
                    pass
        self.df = pd.concat(self.df_lst, axis=0).reset_index(drop=True)
        del self.df_lst

    def __check_non_overlapping_annotations(self):
        shifted_annotations = deepcopy(self.clf_annotations)
        shifted_annotations['START'] = self.clf_annotations['START'].shift(-1)
        shifted_annotations = shifted_annotations.head(-1)
        return shifted_annotations.query('START < STOP')

    def run(self):
        """
        Method to append BORIS annotations created in :meth:`~simba.BorisAppender.create_boris_master_file` to the
        featurized pose-estimation data in the SimBA project. Results (parquets' or CSVs) are saved within the the
        project_folder/csv/targets_inserted directory of the SimBA project.
        """
        for file_cnt, file_path in enumerate(self.feature_file_paths):
            _, self.video_name, _ = get_fn_ext(file_path)
            print('Appending BORIS annotations to {} ...'.format(self.video_name))
            data_df = read_df(file_path, self.file_type)
            self.out_df = deepcopy(data_df)
            video_annot = self.df.loc[self.df[MEDIA_FILE_PATH] == self.video_name]
            video_annot = video_annot.loc[(video_annot[STATUS] == START) | (video_annot[STATUS] == STOP)]

            if self.error_settings[Methods.ADDITIONAL_THIRD_PARTY_CLFS.value] != Dtypes.NONE.value:
                additional_third_party_clf_test(project_clfs=self.clf_names,
                                                annotator_clfs=list(set(self.df[BEHAVIOR].unique()) - set(self.clf_names)),
                                                annotator='BORIS',
                                                error_type=self.error_settings[Methods.ADDITIONAL_THIRD_PARTY_CLFS.value])





            additional_clfs = list(set(self.df[BEHAVIOR].unique()) - set(self.clf_names))
            if self.error_settings[Methods.ADDITIONAL_THIRD_PARTY_CLFS.value] == Methods.WARNING.value and additional_clfs:
                ThirdPartyAnnotationsAdditionalClfWarning(video_name='', clf_names=additional_clfs)




    #         vid_annotations = vid_annotations[vid_annotations['Behavior'].isin(self.clf_names)]
    #         if (len(vid_annotations) == 0):
    #             print('SIMBA WARNING: No BORIS annotations detected for SimBA classifier(s) named {} for video {}'.format(str(self.clf_names), self.video_name))
    #             continue
    #         video_fps = vid_annotations['FPS'].values[0]
    #         for clf in self.clf_names:
    #             self.clf = clf
    #             clf_annotations = vid_annotations[(vid_annotations['Behavior'] == clf)]
    #             clf_annotations_start = clf_annotations[clf_annotations['Status'] == 'START'].reset_index(drop=True)
    #             clf_annotations_stop = clf_annotations[clf_annotations['Status'] == 'STOP'].reset_index(drop=True)
    #             if len(clf_annotations_start) != len(clf_annotations_stop):
    #                 raise ThirdPartyAnnotationEventCountError(video_name=self.video_name, clf_name=self.clf, start_event_cnt=len(clf_annotations_start), stop_event_cnt=len(clf_annotations_stop))
    #             self.clf_annotations = clf_annotations_start['Time'].to_frame().rename(columns={'Time': "START"})
    #             self.clf_annotations['STOP'] = clf_annotations_stop['Time']
    #             self.clf_annotations = self.clf_annotations.apply(pd.to_numeric)
    #             results = self.__check_non_overlapping_annotations()
    #             if len(results) > 0:
    #                 raise ThirdPartyAnnotationOverlapError(video_name=self.video_name, clf_name=self.clf)
    #             self.clf_annotations['START_FRAME'] = (self.clf_annotations['START'] * video_fps).astype(int)
    #             self.clf_annotations['END_FRAME'] = (self.clf_annotations['STOP'] * video_fps).astype(int)
    #             if len(self.clf_annotations) == 0:
    #                 self.out_df[clf] = 0
    #                 print(f'SIMBA WARNING: No BORIS annotation detected for video {self.video_name} and behavior {clf}. SimBA will set all frame annotations as absent.')
    #                 continue
    #             annotations_idx = list(self.clf_annotations.apply(lambda x: list(range(int(x['START_FRAME']), int(x['END_FRAME']) + 1)), 1))
    #             annotations_idx = [x for xs in annotations_idx for x in xs]
    #             idx_difference = list(set(annotations_idx) - set(self.out_df.index))
    #             if len(idx_difference) > 0:
    #                 ThirdPartyAnnotationsOutsidePoseEstimationDataWarning(video_name=self.video_name,
    #                                                                       clf_name=clf,
    #                                                                       frm_cnt=self.out_df.index[-1],
    #                                                                       first_error_frm=idx_difference[0],
    #                                                                       ambiguous_cnt=len(idx_difference))
    #                 annotations_idx = [x for x in annotations_idx if x not in idx_difference]
    #             self.out_df[clf] = 0
    #             self.out_df.loc[annotations_idx, clf] = 1
    #         self.__save_boris_annotations()
    #     self.timer.stop_timer()
    #     print(f'SIMBA COMPLETE: BORIS annotations appended to dataset and saved in project_folder/csv/targets_inserted directory (elapsed time: {self.timer.elapsed_time_str}s).')
    #
    # def __save_boris_annotations(self):
    #     save_path = os.path.join(self.targets_folder, self.video_name + '.' + self.file_type)
    #     save_df(self.out_df, self.file_type, save_path)
    #     print('Saved BORIS annotations for video {}...'.format(self.video_name))

# settings = {'log': False, 'errors': {'ADDITIONAL third-party behavior detected': 'WARNING', 'ZERO third-party video annotations found': 'NONE', 'Annotations and pose FRAME COUNT conflict': 'NONE', 'Annotations EVENT COUNT inconsistency': 'NONE', 'Annotations OVERLAP inaccuracy': 'NONE', 'Annotations data NOT FOUND': 'NONE', 'INVALID annotations file data format': 'NONE'}}
#
# test = BorisAppender(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
#                      data_dir='/Users/simon/Downloads/FIXED', settings=settings)
# test.create_boris_master_file()
# test.run()

# test = BorisAppender(config_path='/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini', boris_folder=r'/Users/simon/Desktop/troubleshooting/train_model_project/boris_import')
# test.create_boris_master_file()
# test.append_boris()

# test = BorisAppender(config_path='/Users/simon/Desktop/envs/marcel_boris/project_folder/project_config.ini', boris_folder=r'/Users/simon/Desktop/envs/marcel_boris/BORIS_data')
# test.create_boris_master_file()
# test.append_boris()

# test = BorisAppender(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
#                      boris_folder='/Users/simon/Downloads/FIXED')
# test.create_boris_master_file()
# test.append_boris()
