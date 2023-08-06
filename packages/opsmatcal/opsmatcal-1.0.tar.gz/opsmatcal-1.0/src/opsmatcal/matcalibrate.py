# Program for calibrating openseespy uniaxial materials
# Version: 0.9
# Date: March 2023

import matplotlib.pyplot as plt
import numpy as np
import openseespy.opensees as ops
import os
import re
import random
from datetime import datetime

class unimatcalibrate:
    def __init__(self, matcommand, variables, file_strain, file_stress, ga_instance):
        self.matCommand = matcommand
        self.File_Strains = file_strain
        self.File_Stresses = file_stress
        self.Variables = variables
        self.GAInstance = ga_instance

    def run(self, num_runs=1, fun_solution=None, previousPop=False,  file_save_solution='solution.txt', file_save_stress='strain_stress.txt'):
       start_time = datetime.now().replace(microsecond=0)
       if num_runs <= 0:
           num_runs = 1
           print('num_Run was set to 1')
       if type(num_runs) == float:
            num_runs = int(num_runs)
            print('num_Run was set to ', num_runs)

       strain, stress = self.__getstrainstress()
       global gennumber
       global perrun
       gennumber = 1
       perrun = 0
       def fitness_func(solution, solution_idx):
           global gennumber
           global perrun
           perrun_ = round(100 * gennumber / self.GAInstance.num_generations / self.GAInstance.sol_per_pop / num_runs, 1)
           if perrun < perrun_:
               perrun = perrun_
               print(str(perrun) + ' %')
           gennumber += 1
           stress_ = self.__calcstress(solution, strain)

           s = 0.0
           for i in range(len(stress_)):
               s += (stress_[i] - stress[i]) ** 2
           fitness = 1 / s
           return fitness

       allsolutions = []
       allfitnesses = []
       ga_instance = self.GAInstance
       ga_instance.fitness_func = fitness_func

       for j in range(num_runs):
           ga_instance.run()
           if previousPop:
               inipop = ga_instance.population
               ga_instance.initial_population = inipop

           solution_, solution_fitness_, solution_idx_ = ga_instance.best_solution()
           allsolutions.append(solution_)
           allfitnesses.append(solution_fitness_)

       if num_runs == 1:
           solution_final = solution_
       else:
           if fun_solution == None:
               bindex = np.argmax(allfitnesses)
               solution_final = allsolutions[bindex]
           else:
               solution_final = fun_solution(allsolutions)

       print('100.0 %')
       self.__printsolution(solution_final)
       self.__savesolution(file_save_solution, file_save_stress, solution_final, strain)
       self.plotsolution(solution_final)

       end_time = datetime.now().replace(microsecond=0)
       print('Start Time: {}'.format(start_time))
       print('End Time: {}'.format(end_time))
       print('Duration: {}'.format(end_time - start_time))

       return solution_final, allsolutions, allfitnesses

    def plotsolution(self, solution):
        strain, stress = self.__getstrainstress()
        stress_ = self.__calcstress(solution, strain)

        fig1 = plt.figure(dpi=200)
        ax1 = plt.axes()
        ax1.plot(strain, stress, linewidth=1, linestyle="--", color='r')
        ax1.plot(strain, stress_, linewidth=1, color='b')
        ax1.set_xlabel("Strain / Displacement")
        ax1.set_ylabel("Stress / Force")
        ax1.legend(['Experimental', 'Calibrated'])
        ax1.grid(True)

        fig2 = plt.figure(dpi=200)
        ax2 = plt.axes()
        ax2.plot(range(len(stress)), stress, linewidth=1, linestyle="--", color='r')
        ax2.plot(range(len(stress_)), stress_, linewidth=1, color='b')
        ax2.set_xlabel("Step")
        ax2.set_ylabel("Stress / Force")
        ax2.legend(['Experimental', 'Calibrated'])
        ax2.grid(True)
        plt.show()

    ##  Stress And Strain
    def __getstrainstress(self):
        file_strain, file_stress = self.File_Strains, self.File_Stresses
        strain = []
        stress = []
        with open(file_strain) as f:
            lines = f.readlines()
        for line in lines:
            line2 = line.split(" ")
            strain.append(float(line2[0]))
        f.close()

        with open(file_stress) as f:
            lines = f.readlines()
        for line in lines:
            line2 = line.split(" ")
            stress.append(float(line2[0]))
        f.close()

        return strain, stress

    def __getStress(self,matcommand_, strain_):
        logfilename = 'opslogfile.txt'
        ops.logFile(logfilename, '-noEcho')
        ops.wipe()
        if isinstance(matcommand_, list):
            for mat_comm in matcommand_:
                eval(mat_comm)
        else:
            eval(matcommand_)
        ops.testUniaxialMaterial(1)
        stress = []
        for eps in strain_:
            ops.setStrain(eps)
            stress.append(ops.getStress())

        return stress

    ## Calculate Stresses
    def __calcstress(self, solution_, strain_):
        if isinstance(self.matCommand, list):
            mat_commands = []
            num_mats = len(self.matCommand)
            st_vars = 0
            for i in range(num_mats):
                mat_vars = self.Variables[i]
                num_vars = len(mat_vars.keys())
                mat_comm = self.matCommand[i]
                mat_comm = 'ops.' + mat_comm
                mat_sol = solution_[st_vars: st_vars + num_vars]
                for j in range(len(mat_sol)):
                    mat_comm = re.sub(r"\b%s\b" % list(mat_vars.keys())[j], str(mat_sol[j]), mat_comm)
                mat_commands.append(mat_comm)
                st_vars += num_vars

            stress_ = self.__getStress(mat_commands, strain_)
        else:
            matcommand_ = 'ops.' + self.matCommand
            for i in range(len(solution_)):
                matcommand_ = re.sub(r"\b%s\b" % list(self.Variables.keys())[i], str(solution_[i]), matcommand_)

            stress_ = self.__getStress(matcommand_, strain_)
        return stress_

    def __printsolution(self, solution_final):
        print('Final Solusion: ')
        if isinstance(self.Variables, list):
            mat_commands = []
            num_mats = len(self.matCommand)
            st_vars = 0
            for i in range(num_mats):
                mat_vars = self.Variables[i]
                num_vars = len(mat_vars.keys())
                mat_comm = self.matCommand[i]
                mat_comm = 'ops.' + mat_comm
                mat_sol = solution_final[st_vars: st_vars + num_vars]
                print('# Material ' + str(i + 1) + ':' + '\n')
                print(mat_comm + '\n')
                for j in range(len(mat_sol)):
                    print(str(list(mat_vars.keys())[j]) + ' = ' + str(mat_sol[j]) + '\n')
                st_vars += num_vars

        else:
            print(self.matCommand + '\n')
            for i in range(len(solution_final)):
                print(str(list(self.Variables.keys())[i]) + ' = ' + str(solution_final[i]) + '\n')

    def __savesolution(self, file_save_solution, file_save_stress, solution_final, strain_):
        if file_save_solution != '':
            if os.path.exists(file_save_solution):
              os.remove(file_save_solution)

            f = open(file_save_solution, "w")

            if isinstance(self.Variables, list):
                mat_commands = []
                num_mats = len(self.matCommand)
                st_vars = 0
                for i in range(num_mats):
                    mat_vars = self.Variables[i]
                    num_vars = len(mat_vars.keys())
                    mat_comm = self.matCommand[i]
                    mat_comm = 'ops.' + mat_comm
                    mat_sol = solution_final[st_vars: st_vars + num_vars]
                    f.write('# Material ' + str(i + 1) + ':' + '\n')

                    for j in range(len(mat_sol)):
                        f.write(str(list(mat_vars.keys())[j]) + ' = ' + str(mat_sol[j]) + '\n')
                    st_vars += num_vars
                    f.write(mat_comm + '\n')
                    f.write('\n')

            else:

                for i in range(len(solution_final)):
                    f.write(str(list(self.Variables.keys())[i]) + ' = ' + str(solution_final[i]) + '\n')
                f.write(self.matCommand + '\n')

            f.close()

        if file_save_stress != '':
            stress_ = self.__calcstress(solution_final, strain_)
            if os.path.exists(file_save_stress):
              os.remove(file_save_stress)

            f = open(file_save_stress, "w")
            for i in range(len(strain_)):
                f.write(str(strain_[i]) + ' , ' + str(stress_[i]) + '\n')

            f.close()
def uniMatTester(ops,matTag, strain, stress=[]):
    logfilename = 'opslogfile.txt'
    ops.logFile(logfilename, '-noEcho')
    # ops.wipe()
    ops.testUniaxialMaterial(matTag)
    stress_ = []
    for eps in strain:
        ops.setStrain(eps)
        stress_.append(ops.getStress())

    fig2 = plt.figure(dpi=200)
    ax2 = plt.axes()
    if len(stress) != 0:
        ax2.plot(range(len(stress)), stress, linewidth=1, linestyle="--", color='r')
    ax2.plot(range(len(stress_)), stress_, linewidth=1, color='b')
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Stress / Force")
    if len(stress) != 0:
        ax2.legend(['Experimental', 'Calibrated'])
    ax2.grid(True)

    fig1 = plt.figure(dpi=200)
    ax1 = plt.axes()
    if len(stress) != 0:
         ax1.plot(strain, stress, linewidth=1, linestyle="--", color='r')
    ax1.plot(strain, stress_, linewidth=1, color='b')
    ax1.set_xlabel("Strain / Displacement")
    ax1.set_ylabel("Stress / Force")
    if len(stress) != 0:
        ax1.legend(['Experimental', 'Calibrated'])
    ax1.grid(True)


    plt.show()

    return stress_

def fitness_func(solution, solution_idx):
    pass

def initial_population(num_poulation, variables):
    inipop = []
    for k in range(num_poulation):
        pop_ = []
        if isinstance(variables, list):
            for vars in variables:
                for vals in vars.values():
                    pop_.append(random.random() * (vals[1] - vals[0]) + vals[0])
        else:
            for vals in variables.values():
                pop_.append(random.random() * (vals[1] - vals[0]) + vals[0])
        inipop.append(pop_)

    return inipop

def gen_space(variables):
    gene_space_ = []
    if isinstance(variables, list):
        for vars in variables:
            for vals in vars.values():
                gene_space_.append({'low': vals[0], 'high': vals[1]})
    else:
        for vals in variables.values():
            gene_space_.append({'low': vals[0], 'high': vals[1]})

    return gene_space_