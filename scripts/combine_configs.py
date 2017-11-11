#!/usr/bin/env python

import yaml
import click

@click.command()
@click.argument('configs', nargs=-1)
@click.option('--prepend-str', '-s', required=False, type=click.STRING,
              help=('Strings to prepend sample names by per config file. \n'
                    'Comma-delimited per config'))
@click.option('--params', '-p', type=click.Path(exists=True), required=True,
              help='Specify parameters for the tools in a YAML file.')
@click.option('--envs', '-e', type=click.Path(exists=True), required=True,
              help='Specify environments for the tools in a YAML file.')
@click.option('--combine-reads', '-c', is_flag=True, default=False,
              help='When sample present in multiple configs, combine reads.')
@click.option('--local-scratch', type=click.Path(),
              default='/tmp',
              help='Temporary directory for storing intermediate files.')
@click.option('--output', '-o', type=click.Path(resolve_path=True,
              writable=True),
              default='config.yaml',
              required=True,
              help='Combined config file.')

def combine_configs(configs, prepend_str, params, envs, combine_reads,
                    local_scratch, output):

    # PARAMS
    with open(params, 'r') as f:
        params_dict = yaml.load(f)

    # ENVS
    with open(envs, 'r') as f:
        envs_dict = yaml.load(f)

    # Load samples into dicts
    samples_dict = {}

    # spit combine prepends
    prepends = None
    if prepend_str:
        prepends = prepend_str.split(',')
        if len(set(prepends)) == len(prepends):
            raise ValueError('Prepend strings must be unique.')

    for i, config in enumerate(configs):
        with open(config, 'r') as f:
            c_d = yaml.load(f)['samples']

        for sample in c_d:
            # modify sample name with prepend string if applicable
            if prepends:
                sample_name = '{0}_{1}'.format(prepends[i], sample)
            else:
                sample_name = sample

            # check to see if collision
            if sample_name in samples_dict and not combine_reads:
                raise ValueError('Sample %s duplicated in two configs. Must '
                                 'either allow read merging with --combine-'
                                 'reads or provide unique prepend strings.')
            # if collision AND add reads, add reads
            elif sample_name in samples_dict and combine_reads:
                samples_dict[sample_name]['forward'].extend(c_d[sample]['forward'])
                samples_dict[sample_name]['reverse'].extend(c_d[sample]['reverse'])
            # else no collision, add reads
            else:
                samples_dict[sample_name] = c_d[sample]

    config_dict = {}
    config_dict['samples'] = samples_dict
    config_dict['params'] = params_dict
    config_dict['envs'] = envs_dict
    config_dict['tmp_dir_root'] = local_scratch

    config_yaml = yaml.dump(config_dict, default_flow_style=False)

    with open(output, 'w') as f:
        f.write(config_yaml)

if __name__ == '__main__':
    combine_configs()
