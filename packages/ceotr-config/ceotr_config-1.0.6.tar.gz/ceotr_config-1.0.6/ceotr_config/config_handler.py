import os
import yaml
import copy
import json


def check_create_dir(file_dir, recursively=False):
    """
    If dir exist just return the path, else create the dir and return the path
    """
    if not os.path.isdir(file_dir):
        if recursively:
            os.makedirs(file_dir)
        else:
            os.mkdir(file_dir)
    return file_dir


def setting_file_path_validation(setting_path):
    check_create_dir(os.path.dirname(setting_path), recursively=True)
    file_name = os.path.basename(setting_path)
    if not file_name.endswith(".yml"):
        msg = "Given setting name {} must end with .yml".format(setting_path)
        raise ValueError(msg)


class ConfigHandler(object):

    def __init__(self, setting_path, template_dir, default_template_name, check_value_update=False):
        """
        :param setting_path: Setting file path for the project
        :param template_dir:
        :param default_template_name: Default template name, the template is under app_common.config.template
        """
        self.template_path = template_dir
        self.default_template_name = default_template_name
        self.setting_path = setting_path
        self.check_value_update = check_value_update
        setting_file_path_validation(setting_path)
        self.yml_config = None
        self.possible_unchanged_field = []

    def build_or_load(self):
        """
        Check the target yml,
        if it is ok, load the yml
        :return:
        """
        user_tpl = self.check_user_yml_template()
        default_yml_template = self.load_default_yml_template()
        merged_yml_template = self.merge_yml(default_yml_template, user_tpl)
        try:
            if not os.path.isfile(self.setting_path):
                dump_yml_to_path(self.setting_path, merged_yml_template)
                msg = "Please fill all the required info at {}".format(self.setting_path)
                raise FileNotFoundError(msg)
            else:
                cfg = load_yml_from_path(self.setting_path)
                is_yml_template_updated = self.is_yaml_dict_different(merged_yml_template, cfg)
                if is_yml_template_updated:
                    new_merged_yaml = self.merge_yml(merged_yml_template, cfg)
                    dump_yml_to_path(self.setting_path, new_merged_yaml)
                    msg = "Config file updated, please fill in the new required info {}".format(self.setting_path)
                    raise ValueError(msg)
                self.yml_config = load_yml_from_path(self.setting_path)
                if self.check_value_update:
                    self.find_unchanged_field()
                return self.yml_config
        except FileNotFoundError as e:
            if self._if_sys_value_contain(merged_yml_template):
                self.setup_value_from_sys_environment(merged_yml_template)
                return self.yml_config
            else:
                raise e
        except ValueError as e:
            if self._if_sys_value_contain(merged_yml_template):
                self.setup_value_from_sys_environment(merged_yml_template)
                return self.yml_config
            else:
                raise e

    def setup_value_from_sys_environment(self, merged_yml_template):
        for name in merged_yml_template:
            merged_yml_template[name] = json.loads(os.environ[name])
        self.yml_config = merged_yml_template

    def _if_sys_value_contain(self, merged_yml_template):
        os_env = os.environ
        for name in merged_yml_template:
            if name not in os.environ:
                return False
        else:
            return True

    def _find_unchanged_field(self, target_dict):
        for key, item in target_dict.items():
            if type(item) is dict:
                self._find_unchanged_field(item)
            else:
                if type(item) is str:
                    if key.lower() == item.lower():
                        self.possible_unchanged_field.append(key)

    def find_unchanged_field(self):
        self._find_unchanged_field(self.yml_config)
        if self.possible_unchanged_field:
            msg = "The key and value are the same for fields {} in the config {}. You may need to change these fields from their default values."
            fields = ", ".join(self.possible_unchanged_field)
            msg = msg.format(fields, self.setting_path)
            raise ValueError("some file didn't change {}".format(msg))

    def load_default_yml_template(self):
        tpl_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")
        tpl_path = os.path.join(tpl_dir_path, self.default_template_name)
        tpl_yml_dict = load_yml_from_path(tpl_path)
        return tpl_yml_dict

    def merge_yml(self, target_yml, merge_into_yml):
        """
        merge first yml into second yml,
        if both yml has same value, use value from second yml
        :param target_yml:
        :param merge_into_yml:
        :return:
        """
        merged_yml = copy.deepcopy(merge_into_yml)
        if merged_yml:
            for default_yml_key, default_yml_value in target_yml.items():
                if default_yml_key in merge_into_yml:
                    for key, item in default_yml_value.items():
                        if key not in merge_into_yml[default_yml_key]:
                            merged_yml[default_yml_key][key] = item
                else:
                    merged_yml[default_yml_key] = default_yml_value
        else:
            return target_yml
        return merged_yml

    def is_yaml_dict_different(self, yml1, yml2):
        """
        Compare two yaml dict to see if the yaml structure is difference (compare key only)
        :param yml1:
        :param yml2:
        :return: True for is different and False means it is same
        """
        DIFFERENT = True
        SAME = False
        difference = SAME
        if type(yml1) is not dict and type(yml2) is not dict:
            return SAME
        elif type(yml1) is dict and type(yml2) is dict:
            for key, value in yml1.items():
                if key in yml2:
                    difference = self.is_yaml_dict_different(value, yml2[key])
                else:
                    difference = DIFFERENT
                if difference is DIFFERENT:
                    return DIFFERENT
            else:
                return SAME
        else:
            difference = DIFFERENT
            return difference

    def compare_and_merge_yamls(self, tpl_yml, target_yml):
        difference = False
        for tpl_key, tpl_value in tpl_yml.items():
            if target_yml and tpl_key in target_yml:
                target_value = target_yml[tpl_key]
                for tpl_value_key in tpl_value:
                    if tpl_value_key in target_value:
                        tpl_value[tpl_value_key] = target_value[tpl_value_key]
                    else:
                        difference = True
            else:
                difference = True

        if difference:
            return tpl_yml
        else:
            return False

    def check_user_yml_template(self):
        if os.path.isfile(self.template_path):
            user_yml_template_obj = load_yml_from_path(self.template_path)
            return user_yml_template_obj
        else:
            msg = 'User Setting Yml template {} does not exist'.format(self.template_path)
            raise FileNotFoundError(msg)

    def _exam_the_value(selfm, section, res):
        for key, value in res.items():
            if not value:
                msg = "Please fill info for {} {}:".format(section, key)
                raise ValueError(msg)


def read_file_as_str(file_path):
    with open(file_path, 'r') as myfile:
        data = myfile.read()
    return data


def load_yml_from_path(file_path):
    with open(file_path, 'r') as stream:
        tpl_yml_dict = yaml.safe_load(stream)
    return tpl_yml_dict


def dump_yml_to_path(file_path, content):
    with open(file_path, 'w') as f:
        yaml.dump(content, f, default_flow_style=False)
