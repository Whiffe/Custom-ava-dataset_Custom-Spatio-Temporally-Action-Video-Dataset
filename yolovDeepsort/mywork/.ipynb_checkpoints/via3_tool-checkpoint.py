# -*- coding: utf-8 -*-
# 文件格式参考: https://gitlab.com/vgg/via/-/blob/via-3.x.y/via-3.x.y/CodeDoc.md#structure-of-via-project-json-file
import json
from collections import defaultdict

class Via3Json(object):
    def __init_load(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as json_fd:
            self.ann_dict = json.load(json_fd)
        self.projects = self.ann_dict['project']
        self.configs = self.ann_dict['config']
        self.attributes = self.ann_dict['attribute']
        self.views = self.ann_dict['view']
        self.metadatas = self.ann_dict['metadata']
        self.files = self.ann_dict['file']

        vid2metadatas=defaultdict(list)
        for  metadata_key in  self.metadatas:
            vid = self.metadatas[metadata_key]['vid']
            if vid in vid2metadatas:
                vid2metadatas[vid].append(self.metadatas[metadata_key])
            else:
                vid2metadatas[vid]=[self.metadatas[metadata_key]]
        self.vid2metadatas = vid2metadatas

    def __init_dump(self, json_path):
        self.json_path = json_path
        self.projects = dict()
        self.configs =dict()
        self.attributes=dict()
        self.files=dict()
        self.metadatas=dict()
        self.views=dict()


    def __init__(self, json_path, mode='load'):
        if mode=='load':
            self.__init_load(json_path)
        elif mode=='dump':
            self.__init_dump(json_path)
        else:
            raise Exception('mode can only provide load or b')

    def loadIdsFromAttsname(self, atts_name):
        assert isinstance(atts_name,(list,tuple,str))
        if type(atts_name) == str:
            atts_name = [atts_name]
        ids = []
        for att_name in  atts_name:
            for id in self.attributes:
                attribute = self.attributes[id]
                if att_name == attribute['aname']:
                    ids.append(id)
        return ids

    def loadOptidsFromAtt(self,att, options_name):
        assert isinstance(options_name,(list,tuple,str))
        if type(options_name) == str:
            options_name = [options_name]
        ids = []
        for option_name in  options_name:
            for option_key in att['options']:
                if option_name == att['options'][option_key]:
                    ids.append(option_key)
        return ids


    def loadFilesFid(self):
        fids = []
        for fid in  self.ann_dict['file']:
            fids.append(fid)
        return fids

    def loadAttFromId(self, id):
        return self.attributes[id]

    def loadAttsFromAll(self):
        return self.attributes

    def loadFileInfoFromFid(self,fid):
        return self.files[fid]

    def loadFilesInfoFromAll(self):
        return self.files

    def loadMetadataInfoFromVid(self, vid):
        return self.vid2metadatas[vid]

    def loadMetadatasInfoFromAll(self):
        return self.vid2metadatas

    def dumpPrejects(self, vid_list, pid='__VIA_PROJECT_ID__', rev='__VIA_PROJECT_REV_ID__',
                     rev_timestamp='__VIA_PROJECT_REV_TIMESTAMP__',pname='Unnamed VIA Project',
                     creator='VGG Image Annotator (http://www.robots.ox.ac.uk/~vgg/software/via)',
                     created=1618642823079):
        assert isinstance(vid_list, (list,))
        for  vid in vid_list:
            assert isinstance(vid, (str,))
        self.projects['pid'], self.projects['rev'] = pid, rev
        self.projects['rev_timestamp'] = rev_timestamp
        self.projects['pname'], self.projects['creator'] =  pname, creator
        self.projects['created'], self.projects['vid_list'] = created, vid_list

    def dumpConfigs(self, file=dict(loc_prefix={ '1':'', '2':'', '3':'', '4':''}),
                          ui=dict(file_content_align='center',
                                  file_metadata_editor_visible=True,
                                  spatial_metadata_editor_visible=True,
                                  spatial_region_label_attribute_id	='',
                                  gtimeline_visible_row_count="4")
                    ):
        self.configs['file'] = file
        self.configs['ui'] = ui

    def dumpAttributes(self, attributes_dict):
        assert isinstance(attributes_dict,(dict,))
        for i, attribute_key in enumerate(attributes_dict, 1):
            attribute = attributes_dict[attribute_key]
            assert attribute.get('aname',False)
            assert attribute.get('type',False) and 1<=attribute['type']<=5 # attributes's user input type ('TEXT':1, 'CHECKBOX':2, 'RADIO':3, 'SELECT':4, 'IMAGE':5 )
            assert attribute.get('options',False)
            _VIA_ATTRIBUTE_ANCHOR = {
                'FILE1_Z0_XY0': 'Attribute of a File (e.g. image caption)',
                'FILE1_Z0_XY1': 'Spatial Region in an Image (e.g. bounding box of an object)',
                'FILE1_Z0_XYN': '__FUTURE__',  # File region composed of multiple disconnected regions
                'FILE1_Z1_XY0': '__FUTURE__',  # Time marker in video or audio (e.g tongue clicks, speaker diarisation)
                'FILE1_Z1_XY1': 'Spatial Region in a Video Frame (e.g. bounding box of an object)',
                'FILE1_Z1_XYN': '__FUTURE__',  # A video frame region composed of multiple disconnected regions
                'FILE1_Z2_XY0': 'Temporal Segment in Video or Audio (e.g. video segment containing an actor)',
                'FILE1_Z2_XY1': '__FUTURE__',  # A region defined over a temporal segment
                'FILE1_Z2_XYN': '__FUTURE__',  # A temporal segment with regions defined for start and end frames
                'FILE1_ZN_XY0': '__FUTURE__',  # ? (a possible future use case)
                'FILE1_ZN_XY1': '__FUTURE__',  # ? (a possible future use case)
                'FILE1_ZN_XYN': '__FUTURE__',  # ? (a possible future use case)
                'FILEN_Z0_XY0': 'Attribute of a Group of Files (e.g. given two images, which is more sharp?)',
                'FILEN_Z0_XY1': '__FUTURE__',  # ? (a possible future use case)
                'FILEN_Z0_XYN': '__FUTURE__',  # one region defined for each file (e.g. an object in multiple views)
                'FILEN_Z1_XY0': '__FUTURE__',  # ? (a possible future use case)
                'FILEN_Z1_XY1': '__FUTURE__',  # ? (a possible future use case)
                'FILEN_Z1_XYN': '__FUTURE__',  # ? (a possible future use case)
                'FILEN_Z2_XY0': '__FUTURE__',  # ? (a possible future use case)
                'FILEN_Z2_XY1': '__FUTURE__',  # ? (a possible future use case)
                'FILEN_Z2_XYN': '__FUTURE__',  # ? (a possible future use case)
                'FILEN_ZN_XY0': '__FUTURE__',  # one timestamp for each video or audio file (e.g. for alignment)
                'FILEN_ZN_XY1': '__FUTURE__',  # ? (a possible future use case)
                'FILEN_ZN_XYN': '__FUTURE__',  # a region defined in a video frame of each video
            }
            assert attribute.get('anchor_id',False) and (attribute.get('anchor_id') in _VIA_ATTRIBUTE_ANCHOR)
            if not attribute.get('desc',False):
                attribute['desc'] = ''
            if not attribute.get('default_option_id',False):
                attribute['default_option_id'] = '0'
        self.attributes = attributes_dict


    def dumpFiles(self, files_dict):
        assert isinstance(files_dict,(dict,))
        for i, files_key in enumerate(files_dict, 1):
            assert isinstance(files_dict[files_key], (dict,))
            file_dict = files_dict[files_key]
            assert file_dict.get('fname', False)
            assert file_dict.get('type', False) #  file type { IMAGE:2, VIDEO:4, AUDIO:8 }

            if not file_dict.get('fid', False):
                file_dict['fid'] = str(i)

            if not file_dict.get('loc', False):   #file location { LOCAL:1, URIHTTP:2, URIFILE:3, INLINE:4 }
                file_dict['loc'] = 1

            if not file_dict.get('src', False):
                file_dict['src'] = ''
        self.files = files_dict

    def dumpMetedatas(self, metadatas_dict):
        assert isinstance(metadatas_dict,(dict,))
        for i, metadatas_key in enumerate(metadatas_dict, 1):
            assert isinstance(metadatas_dict, (dict,))
            metadata_dict = metadatas_dict[metadatas_key]
            assert metadata_dict.get('vid', False)
            assert metadata_dict.get('z', False) or metadata_dict.get('xy', False) # z defines temporal location in audio or video, here it records a temporal segment from 2 sec. to 6.5 sec.
            assert metadata_dict.get('av', False)  and  isinstance(metadata_dict['av'],(dict,))

            if not metadata_dict.get('flg', False):
                metadata_dict['flg'] = 0

            if not metadata_dict.get('z', False):   #file location { LOCAL:1, URIHTTP:2, URIFILE:3, INLINE:4 }
                metadata_dict['z'] = []

            if not metadata_dict.get('xy', False):   #file location { LOCAL:1, URIHTTP:2, URIFILE:3, INLINE:4 }
                metadata_dict['xy'] = []
        self.metadatas = metadatas_dict

    def dumpViews(self, views_dict):
        assert isinstance(views_dict,(dict,))
        for i, views_key in enumerate(views_dict, 1):
            assert isinstance(views_dict, (dict,))
            view_dict = views_dict[views_key]
            assert view_dict.get('fid_list', False) and isinstance(view_dict.get('fid_list'), (list,))
        self.views = views_dict

    def dempJsonSave(self):

        json_infos = {
            'project': self.projects,
            'config': self.configs,
            'attribute':self.attributes,
            'file': self.files,
            'metadata': self.metadatas,
            'view': self.views,
        }

        with open(self.json_path, 'w') as json_file:
            json.dump(json_infos, json_file)


if __name__ == '__main__':
    pass
    # 读取注释文件的示例代码

    # 写入注释文件的示例代码