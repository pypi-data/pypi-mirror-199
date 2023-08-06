from FluxFramework.Metadata import *
from inspect import *

import os
import sys

class MenuBuilder:
    
    @staticmethod
    @register()
    def CheckIsMethodOrFunction(inputObject):
        '''Returns true if the provided object is a method or a function'''
        return ismethod(inputObject) or isfunction(inputObject)
    
    @staticmethod
    @register()
    def OutputMenu(inputObject):
        '''Outputs a menu based on the provided class/module'''
        try:
            availableMethods = getmembers(sys.modules[inputObject.__name__], predicate=MenuBuilder.CheckIsMethodOrFunction)
        except:
            availableMethods = getmembers(inputObject, predicate=MenuBuilder.CheckIsMethodOrFunction)
        sortedMethods = sorted([method[1] for method in availableMethods], key = (lambda field: GetMethodOrder(field)))
        while True:
            try:
                optionNum = 1;
                print("Menu:")
                for method in sortedMethods:
                    print(str(optionNum) + ": " + GetMethodName(method) + ":")
                    print("       " + GetMethodDescription(method))
                    optionNum+=1
                print(str(optionNum) +": Exit")
                print("----------------------------------------")
                choice = int(input("Choose a method to run: "))
                if choice > 0 and choice < optionNum:
                    os.system('cls')
                    try:
                        sortedMethods[choice-1]()
                        input("Press enter to continue...")
                        os.system('cls')
                        return 1
                    except:
                        os.system('cls')
                        print("Failed to invoke method! Choose another option.")
                elif choice == optionNum:
                    return -1
                else:
                    os.system('cls')
                    print("That's not a valid option!")
            except:
                os.system('cls')
                print("That's not a valid option!")