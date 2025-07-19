from mediawiki.mediawiki_create import create_template_from_args

class TockdomTemplate:
    template_name = ""
    required_params = ""

    def to_text(self):
        original_dict = vars(self)
        dict_to_write = original_dict.copy()

        for required_param in self.__class__.required_params:
            if dict_to_write[required_param] is None:
                dict_to_write[required_param] = ""

        for existing_key in list(dict_to_write.keys()):
            new_key = existing_key.replace("_", "-")
            dict_to_write[new_key] = dict_to_write.pop(existing_key)

        return create_template_from_args(dict_to_write, self.__class__.template_name)

    def merge_with_dict(self, params):
        existing_params = list(vars(self).keys())
        for name, value in params.items():
            name = name.replace("-", "_")

            if name not in existing_params:
                raise RuntimeError(f"Param name {name} is not valid.")
            setattr(self, name, value)

    @classmethod
    def from_template_dict(cls, params):
        new_template = cls()
        new_template.merge_with_dict(params)
        return new_template

