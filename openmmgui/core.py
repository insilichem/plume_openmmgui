#!/usr/bin/env python
# encoding: utf-8

# Get used to importing this in your Py27 projects!
from __future__ import print_function, division
# Python
import os
import sys
import yaml
import subprocess

"""
This module contains the business logic of your extension.
Normally, it should contain the Controller and the Model.
Read on MVC design if you don't know about it.
"""


class Controller(object):

    """
    The controller manages the communication
    between the UI (graphic interface)
    and the data model.
    Actions such as clicks on buttons,
    enabling certain areas,
    or runing external programs,
    are the responsibility of the controller.
    """

    def __init__(self, gui, model, *args, **kwargs):
        self.gui = gui
        self.model = model
        self.set_mvc()

    def set_mvc(self):
        self.gui.buttonWidgets['Save Input'].configure(command=self.saveinput)
        self.gui.buttonWidgets['Run'].configure(command=self.run)

    def run(self):
        self.saveinput()
        subprocess.call(['ommprotocol', self.filename])
        sys.stdout.write('MD succesfully finished')

    def saveinput(self):
        self.model.parse()
        self.write()

    def write(self):
        # Write input
        self.filename = os.path.join(self.model.md_output['outputpath'],
                                     self.model.md_output['project_name']+'.yaml')
        with open(self.filename, 'w') as f:
            f.write('# Yaml input for OpenMM MD\n\n')
            f.write('# input\n')
            yaml.dump(self.model.md_input, f, default_flow_style=False)
            f.write('\n')
            f.write('# output\n')
            yaml.dump(self.model.md_output, f, default_flow_style=False)
            if self.model.md_hardware:
                f.write('\n# hardware\n')
                yaml.dump(self.model.md_hardware, f, default_flow_style=False)
            f.write('\n# conditions\n')
            yaml.dump(self.model.md_conditions, f, default_flow_style=False)
            f.write('\n# OpenMM system options\n')
            yaml.dump(self.model.md_systemoptions, f, default_flow_style=False)
            f.write('\n\nstages:\n')
            for stage in self.model.stages:
                yaml.dump([stage], f, indent=8, default_flow_style=False)
                f.write('\n')


class Model(object):

    """The model controls the data we work with.
    Normally, it'd be a Chimera molecule
    and some input files from other programs.
    The role of the model is to create
    a layer around those to allow the easy
    access and use to the data contained in
    those files"""

    def __init__(self, gui, *args, **kwargs):
        self.gui = gui
        self.md_input = {'topology': None,
                         'positions': None,
                         'forcefield': None,
                         'charmm_parameters': None,
                         'velocities': None,
                         'box_vectors': None}

        self.md_output={ 'project_name': None,
                          'restart': None,
                          'trajectory_every': None,
                          'outputpath': None,
                          'report_every': None,
                          'trajectory_every': None,
                          'trajectory_new_every': None,
                          'restart_every': None,
                          'trajectory_atom_subset': None,
                          'report': True,
                          'trajectory': None}

        self.md_hardware={'platform':None,
                          'precision':None}

        self.md_conditions={'timestep': None,
                            'integrator': None,
                            'barostat': False,
                            'temperature': None,
                            'friction': None,
                            'pressure': None,
                            'barostat_interval': None}

        self.md_systemoptions ={ 'nonbondedMethod': None,
                                 'nonbondedCutoff': None,
                                 'ewaldErrorTolerance': None,
                                 'constraints': None,
                                 'rigidWater': False}

    @property
    def stages(self):
        return self.gui.stages

    @property
    def project_name(self):
        return  self.gui.var_output_projectname.get()

    @property
    def topology(self):
        if self.gui.ui_input_note.index(self.gui.ui_input_note.select()) == 0:
            if self.gui.ui_chimera_models.getvalue():
                model = self.gui.ui_chimera_models.getvalue()
                model_name = os.path.splitext(model.name)[0]
                sanitized_path = str(os.path.join(self.gui.var_output.get(), model_name + '_fixed.pdb'))
                if os.path.isfile(sanitized_path):
                    return sanitized_path
                else:
                    return model.openedAs[0]

        elif self.gui.ui_input_note.index(self.gui.ui_input_note.select()) == 1:
                return self.gui.var_path.get()

    @topology.setter
    def topology(self, value):
        if not os.path.isfile(value):
            raise ValueError('Cannot access file {}'.format(value))
        self.gui.var_path.set(value)

    @property
    def positions(self):
        if self.gui.ui_input_note.index(self.gui.ui_input_note.select()) == 0:
            return self.topology
        elif self.gui.ui_input_note.index(self.gui.ui_input_note.select()) == 1:
            return self.gui.var_positions.get()

    @positions.setter
    def positions(self, value):
        if not os.path.isfile(value):
            raise ValueError('Cannot access file {}'.format(value))
        self.gui.var_positions.set(value)

    @property
    def forcefield(self):
        return [self.gui.var_forcefield.get() + '.xml', ] + self.gui.additional_force

    @forcefield.setter
    def forcefield(self, value):
        self.gui.additional_force.set(value)
        self.gui.var_forcefield.set(value)

    @property
    def charmm_parameters(self):
        return self.gui.var_parametrize_forc.get()

    @charmm_parameters.setter
    def charmm_parameters(self, value):
        if not os.path.isfile(value):
            raise ValueError('Cannot access file {}'.format(value))
        self.gui.var_parametrize_forc.set(value)

    @property
    def velocities(self):
        return self.gui.var_input_vel.get()

    @velocities.setter
    def velocities(self, value):
        if not os.path.isfile(value):
            raise ValueError('Cannot access file {}'.format(value))
        self.gui.var_input_vel.set(value)

    @property
    def box_vectors(self):
        return self.gui.var_input_box.get()

    @box_vectors.setter
    def box_vectors(self, value):
        if not os.path.isfile(value):
            raise ValueError('Cannot access file {}'.format(value))
        self.gui.var_input_box.set(value)

    @property
    def restart(self):
        return self.gui.var_output_restart.get()

    @restart.setter
    def restart(self, value):
        if not os.path.isfile(value):
            raise ValueError('Cannot access file {}'.format(value))
        self.gui.var_output_restart.set(value)

    @property
    def outputpath(self):
        return self.gui.var_output.get()

    @outputpath.setter
    def outputpath(self, value):
        self.gui.var_output.set(value)

    @property
    def integrator(self):
        return self.gui.var_integrator.get()

    @integrator.setter
    def integrator(self, value):
        self.gui.var_integrator.set(value)

    @property
    def nonbondedMethod(self):
        return self.gui.var_advopt_nbm.get()

    @nonbondedMethod.setter
    def nonbondedMethod(self, value):
        self.gui.var_advopt_nbm.set(value)

    @property
    def nonbondedCutoff(self):
        return self.gui.var_advopt_cutoff.get()

    @nonbondedCutoff.setter
    def nonbondedCutoff(self, value):
        self.gui.var_advopt_cutoff.set(value)

    @property
    def ewaldErrorTolerance(self):
        return self.gui.var_advopt_edwalderr.get()

    @ewaldErrorTolerance.setter
    def ewaldErrorTolerance(self, value):
        self.gui.var_advopt_edwalderr.set(value)

    @property
    def rigidWater(self):
        return self.gui.var_advopt_rigwat.get()

    @rigidWater.setter
    def rigidWater(self, value):
        self.gui.var_advopt_rigwat.set(value)

    @property
    def constraints(self):
        return self.gui.var_advopt_constr.get()

    @constraints.setter
    def constraints(self, value):
        self.gui.var_advopt_constr.set(value)

    @property
    def platform(self):
        value = self.gui.var_advopt_hardware.get() 
        if value.lower() != 'auto':
            return value

    @platform.setter
    def platform(self, value):
        self.gui.var_advopt_hardware.set(value)

    @property
    def precision(self):
        if self.platform:
            return self.gui.var_advopt_precision.get()

    @precision.setter
    def precision(self, value):
        self.gui.var_advopt_precision.set(value)

    @property
    def timestep(self):
        return self.gui.var_tstep.get()

    @timestep.setter
    def timestep(self, value):
        self.gui.tstep.var_set(value)

    @property
    def barostat(self):
        return self.gui.var_advopt_barostat.get()

    @barostat.setter
    def barostat(self, value):
        self.gui.self.var_advopt_barostat.set(value)

    @property
    def temperature(self):
        return self.gui.var_advopt_temp.get()

    @temperature.setter
    def temperature(self, value):
        self.gui.self.var_advopt_temp.set(value)

    @property
    def friction(self):
        return self.gui.var_advopt_friction.get()

    @friction.setter
    def friction(self, value):
        self.gui.self.var_advopt_friction.set(value)

    @property
    def pressure(self):
        return self.gui.var_advopt_pressure.get()

    @pressure.setter
    def pressure(self, value):
        self.gui.self.var_advopt_pressure.set(value)

    @property
    def barostat_interval(self):
        return self.gui.var_advopt_pressure_steps.get()

    @barostat_interval.setter
    def barostat_interval(self, value):
        self.gui.self.var_advopt_pressure_steps.set(value)

    @property
    def trajectory(self):
        return self.gui.var_md_reporters.get()

    @trajectory.setter
    def trajectory(self, value):
        self.gui.self.var_md_reporters.set(value)


    @property
    def trajectory_every(self):
        if self.trajectory != 'None':
            return self.gui.var_output_traj_interval.get()

    @trajectory_every.setter
    def trajectory_every(self, value):
        self.gui.self.var_output_traj_interval.set(value)

    @property
    def report(self):
        return self.gui.var_verbose.get()

    @property
    def report_every(self):
        if self.report.lower()== 'true':
            return self.gui.var_output_stdout_interval.get()

    @report_every.setter
    def report_every(self, value):
        self.gui.self.var_output_stdout_interval.set(value)

    @property
    def trajectory_new_every(self):
        return self.gui.var_traj_new_every.get()

    @trajectory_new_every.setter
    def trajectory_new_every(self, value):
        self.gui.self.var_traj_new_every.set(value)

    @property
    def restart_every(self):
        return self.gui.var_restart_every.get()

    @restart_every.setter
    def restart_every(self, value):
        self.gui.self.var_restart_every.set(value)

    @property
    def trajectory_atom_subset(self):
        return self.gui.var_traj_atoms.get()

    @trajectory_atom_subset.setter
    def trajectory_atom_subset(self, value):
        self.gui.self.var_traj_atoms.set(value)



    def parse(self):
        self.reset_variables()
        self.retrieve_settings()
        self.retrieve_stages()    

    def retrieve_settings(self):
        dictionaries=[self.md_input, self.md_output, self.md_hardware,
                      self.md_conditions, self.md_systemoptions]
        for dictionary in dictionaries:
            for key, value in dictionary.items():
                # Some combobox just returns boolean as a string so we fix that
                value_to_store = getattr(self, key)
                if value_to_store == 'True':
                    value_to_store = True
                elif value_to_store == 'False':
                    value_to_store = False
                if isinstance(value_to_store, bool):
                    dictionary[key] = value_to_store
                elif value_to_store == 'None':
                    del dictionary[key]
                elif value_to_store:
                    dictionary[key] = value_to_store
                else:
                    del dictionary[key]

    def retrieve_stages(self):
        for dictionary in self.stages:
            for key, value in dictionary.items():
                if value == 'True':
                    value = True
                    dictionary[key] = value
                elif value == 'False':
                    value = False
                    dictionary[key] = value
                elif value in [None,'None']:
                    del dictionary[key]
        self.stages

    def reset_variables(self):
        self.md_input = {'topology': None,
                         'positions': None,
                         'forcefield': None,
                         'charmm_parameters': None,
                         'velocities': None,
                         'box_vectors': None}

        self.md_output = {'project_name': None,
                          'restart': None,
                          'trajectory_every': None,
                          'outputpath': None,
                          'report_every': None,
                          'trajectory_every': None,
                          'trajectory_new_every': None,
                          'restart_every': None,
                          'trajectory_atom_subset': None,
                          'report': True,
                          'trajectory': None}

        self.md_hardware = {'platform': None,
                            'precision': None}

        self.md_conditions = {'timestep': None,
                              'integrator': None,
                              'barostat': False,
                              'temperature': None,
                              'friction': None,
                              'pressure': None,
                              'barostat_interval': None}

        self.md_systemoptions = {'nonbondedMethod': None,
                                 'nonbondedCutoff': None,
                                 'ewaldErrorTolerance': None,
                                 'constraints': None,
                                 'rigidWater': False}