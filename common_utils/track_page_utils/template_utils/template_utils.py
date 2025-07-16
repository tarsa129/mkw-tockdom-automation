from mediawiki.mediawiki_create import create_template_from_args

class TockdomTemplate:
    template_name = ""
    required_params = ""

    def to_text(self):
        original_dict = vars(self)

        for required_param in self.__class__.required_params:
            if original_dict[required_param] is None:
                original_dict[required_param] = ""

        return create_template_from_args(vars(self), self.__class__.template_name)

    def merge_with_dict(self, params):
        existing_params = list(vars(self).keys())
        for name, value in params.items():
            if name not in existing_params:
                raise RuntimeError(f"Param name {name} is not valid.")
            setattr(self, name, value)

    @classmethod
    def from_template_dict(cls, params):
        new_template = cls()
        new_template.merge_with_dict(params)
        return new_template

