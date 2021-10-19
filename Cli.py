from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
import json
from PyInquirer import prompt, Separator


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

class Cli:
    # def __init__(self):
    #     self.manager = Upcloud_api()

    def ask_action(self):
        directions_prompt = {
            'type': 'list',
            'name': 'action',
            'message': 'Which action would you like to perform?',
            'choices': ['CreateVM', 'CheckVmStatus', 'DeleteVm', 'VmConsole','PerformanceStat','VmEvents']
        }
        answers = prompt(directions_prompt)
        return answers['action']

    def ask_zone(self):
        directions_prompt = {
            'type': 'list',
            'name': 'zone',
            'message': 'Which zone would you like to choose?',
            'choices': ['z1', 'z2', 'z3', 'z4','z5','z6']
        }
        answers = prompt(directions_prompt)
        return answers['zone']

    def ask_plan(self):
        directions_prompt = {
            'type': 'list',
            'name': 'plan',
            'message': 'Which plan would you like to choose?',
            'choices': ['p1', 'p2', 'p3', 'p4','p5','p6']
        }
        answers = prompt(directions_prompt)
        return answers['plan']

    def ask_os(self):
        directions_prompt = {
            'type': 'list',
            'name': 'os',
            'message': 'Which os would you like to choose?',
            'choices': ['o1', 'o2', 'o3', 'o4','o5','o6']
        }
        answers = prompt(directions_prompt)
        return answers['os']
    # TODO better to use while loop than recursion!


    def main(self):
        print('You find yourself in a small room, there is a door in front of you.')
        #exit_house()
        action()
    def request_progress(self):
        directions_prompt = {
            'type': 'list',
            'name': 'request_prog',
            'message': '  would you like to monitor the progress of your request?',
            'choices': ['YES','NO']
        }
        answers = prompt(directions_prompt)
        return answers['request_prog']

    def get_vm_details(self):
        vmDetails=[]
        VmNumber = self.vm_number_input()
        for i in range(0, VmNumber):
            vmName = self.vm_name_input()
            zone = self.ask_zone()
            plan = self.ask_plan()
            os = self.ask_os()
            vmDetails.append([vmName, zone, os, plan])
        return vmDetails

    def performe_CreateVM(self):
        vmDetails=self.get_vm_details()
        monitor=self.request_progress()
        self.requestSummary( vmDetails, monitor)



    def action(self):
        action = self.ask_action()
        if (action == 'CreateVM'):
            self.performe_CreateVM()
        elif (action == 'CheckVmStatus'):
            print('CheckVmStatus')
        elif (action == 'DeleteVm'):
            print('DeleteVm')
        elif (action == 'VmConsole'):
            print('VmConsole')
        elif (action == 'PerformanceStat'):
            print('PerformanceStat')
        elif (action == 'VmEvents'):
            print('VmEvents')


    def requestSummary(self,vmDetails,monitor):
        print("..")
        summary=[]
        for i in vmDetails:
            thisdict = {
                "vmNname": i[0],
                "vmZone": i[1],
                "vmPlan": i[2],
                "vmOs": i[3]

            }

            summary.append(thisdict)
        print("=======this is your request choices summary======== \n\n\n")
        print("VMs DETAILS \n\n\n")
        print(summary)
        print("\n\n\n")
        print("MONITORING CHOICE: ",monitor,"\n\n\n")


    def encounter2a(self):
        direction = ask_action()
        if direction == 'Forward':
            output = 'You find a painted wooden sign that says:'
            output += ' \n'
            output += ' ____  _____  ____  _____ \n'
            output += '(_  _)(  _  )(  _ \\(  _  ) \n'
            output += '  )(   )(_)(  )(_) ))(_)(  \n'
            output += ' (__) (_____)(____/(_____) \n'
            print(output)
        else:
            print('You cannot go that way')
            encounter2a()

    def vm_name_input(self):
        questions = [
            {
                'type': 'input',
                'name': 'vmName',
                'message': 'What\'s your VM name',
            }
        ]
        answers = prompt(questions)
        return answers['vmName']


    def vm_number_input(self):
        questions = [
            {
                'type': 'input',
                'name': 'vmNumber',
                'message': 'how many VMs you would like to create',
            }
        ]
        answers = prompt(questions)
        return int(answers['vmNumber'])

    # def encounter2b():
    #     prompt({
    #         'type': 'list',
    #         'name': 'weapon',
    #         'message': 'Pick one',
    #         'choices': [
    #             'Use the stick',
    #             'Grab a large rock',
    #             'Try and make a run for it',
    #             'Attack the wolf unarmed'
    #         ]
    #     },  style=style)
    #     print('The wolf mauls you. You die. The end.')


    # if __name__ == '__main__':
    #     main()
ins=Cli()
ins.performe_CreateVM()
