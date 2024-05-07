from virtmaker.runners.steps.run import Run


class Firstboot(Run):
    _tag = "firstboot"
    _virt_customize_first_arg = '--firstboot'
