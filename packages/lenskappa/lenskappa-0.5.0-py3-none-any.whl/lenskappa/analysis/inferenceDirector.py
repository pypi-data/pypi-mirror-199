
from pathlib import Path


def build_inference_director(configuration, base_configuration, inference_module):
    parameters = configuration.get("parameters", None)
    common = configuration.get("common", None)
    delegate = configuration.get("delegate", None)
    invariant_parameters = {}
    variable_parameters = {}

    delegated_params = {}
    if delegate is not None:
        for name, arguments in delegate.items():
            fname = "_".join(["delegate", name])
            function = getattr(inference_module, fname)
            delegated_params.update({name: function(**arguments)})
    if common is not None:
        common_params = {}
        for name, value in common.items():
            if name.endswith("_base"):
                pname = name.removesuffix("_base")
                common_params.update({pname: handle_base(pname, value, configuration["parameters"])})
                parameters.pop(pname)
            else:
                common_params.update({name: value})
    all_params = ""
    print(parameters)
    exit()
    #print(delegated_params)



def handle_base_path(base_param, params):
    path = Path(base_param)
    return [path / p for p in params]

known_handlers = {
    "path": handle_base_path
}

def handle_base(param_name, base_param, params):
    for name, handler in known_handlers.items():
        if name in param_name:
            return handler(base_param, params[param_name])


class InferenceDirector:
    """
    Often times, we will want to run the same inference several times
    with slight modifications of the parameters. This class allows us
    to do that by keeping track of which inference we're working with,
    and tracking shared parameters (as well as actually running the
    inferences)
    """
    def __init__(self, configurations, base_configuration, inference_module):
        """
        Build an inference list from a configuration, a base configuration, and
        the module the inference is defined in.
        """

if __name__ == "__main__":
    import json 
    from lenskappa.analysis import kappa_inference 

    with open("/Users/patrick/code/Production/environment_study/lenskappa/lenskappa/analysis/kappa_many.json", "r") as f:
        params = json.load(f)
    
    with open("/Users/patrick/code/Production/environment_study/lenskappa/lenskappa/analysis/kappa.json", "r") as f:
        template = json.load(f)

    inf = build_inference_director(params, template, kappa_inference)
    exit()
    bins, pdf = inf.run_inference()
    bin_averages = (bins[1:] + bins[:-1])/2.0
    plt.plot(bin_averages, pdf)
    plt.show()    