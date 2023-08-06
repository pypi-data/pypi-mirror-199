#!/usr/bin/python
# -*- coding: utf-8 -*-

# EnhaaancedLists - Copyright & Contact Notice
##############################################
# Created by Dominik Niedenzu                #      
# Copyright (C) 2021-2023 Dominik Niedenzu   #
#     All Rights Reserved                    #
#                                            #
#           Contact:                         #
#      pyadaaah@blackward.de                 #         
#      www.blackward.de                      #         
##############################################

# EnhaaancedLists - Version & Modification Notice
#################################################
# Based on EnhaaancedLists Version 0.90         #
# Modified by --- (date: ---)                   #
#################################################

# EnhaaancedLists - License
#######################################################################################################################
# Use and redistribution in source and binary forms, without or with modification,                                    #
# are permitted (free of charge) provided that the following conditions are met (including the disclaimer):           #
#                                                                                                                     #
# 1. Redistributions of source code must retain the above copyright & contact notice and                              #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#                                                                                                                     #
#    a) If said source code is redistributed unmodified, the belonging file name must be enhaaancedLists.py and       #
#       said file must retain the above version & modification notice too.                                            #
#                                                                                                                     #
#    b) Whereas if said source code is redistributed modified (this includes redistributions of                       #
#       substantial portions of the source code), the belonging file name(s) must be enhaaancedLists_modified*.py     #
#       (where the asterisk stands for an arbitrary intermediate string) and said files                               #
#       must contain the above version & modification notice too - updated with the name(s) of the change             #
#       maker(s) as well as the date(s) of the modification(s).                                                       #
#                                                                                                                     #
# 2. Redistributions in binary form must reproduce the above copyright & contact notice and                           #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#    They must also reproduce a version & modification notice similar to the one above - in the                       #
#    sense of 1. a) resp. b).                                                                                         #
#                                                                                                                     #
# 3. Neither the name "Dominik Niedenzu", nor the name resp. trademark "Blackward", nor the names of authors resp.    #
#    contributors resp. change makers may be used to endorse or promote products derived from this software without   #
#    specific prior written permission.                                                                               #
#                                                                                                                     #
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO   # 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.                            #
#                                                                                                                     #
# IN NO EVENT SHALL DOMINIK NIEDENZU OR AUTHORS OR CONTRIBUTORS OR CHANGE MAKERS BE LIABLE FOR ANY CLAIM, ANY         # 
# (DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL) DAMAGE OR ANY OTHER LIABILITY, WHETHER IN AN    #
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THIS SOFTWARE (OR PARTS OF THIS   #
# SOFTWARE) OR THE USE OR REDISTRIBUTION OR OTHER DEALINGS IN THIS SOFTWARE (OR PARTS OF THIS SOFTWARE).              #
#                                                                                                                     #
# THE USERS RESP. REDISTRIBUTORS OF THIS SOFTWARE (OR PARTS OF THIS SOFTWARE) ARE SOLELY RESPONSIBLE FOR ENSURING     #
# THAT AFOREMENTIONED CONDITIONS ALL ARE MET AND COMPLIANT WITH THE LAW IN THE RESPECTIVE JURISDICTION - BEFORE (!)   #
# THEY USE RESP. REDISTRIBUTE.                                                                                        #
#######################################################################################################################



#import (from) common libraries
from argparse         import ArgumentParser as Argparse_ArgumentParser
from sys              import version_info   as Sys_version_info
from functools        import partial        as Functools_partial
from operator         import attrgetter     as Operator_attrgetter
from operator         import itemgetter     as Operator_itemgetter
from sys              import stderr         as Sys_stderr
from os               import linesep        as Os_linesep
from threading        import Lock           as Threading_Lock
from threading        import Thread         as Threading_Thread
from multiprocessing  import Lock           as Multiprocessing_Lock
from random           import uniform        as Random_uniform
from random           import shuffle        as Random_shuffle
from time             import sleep          as Time_sleep
from pickle           import dumps          as Pickle_dumps
from pickle           import loads          as Pickle_loads
from math             import factorial      as Math_factorial
from sys              import stdout         as Sys_stdout
from sys              import stderr         as Sys_stderr
from decimal          import Decimal        as Decimal_Decimal
from collections      import namedtuple     as Collections_namedtuple


#python version 2 checker
def isPy2():
    """
         Returns True if Python version in use is < 3.0.
    """
    if    Sys_version_info.major < 3.0:
          return True
    else:
          return False
          
          
#python version 3 checker          
def isPy3():
    """
         Returns True if Python version in use is >= 3.0.
    """
    if    Sys_version_info.major >= 3.0:
          return True
    else:
          return False
          
          
### take differences between python2 and python3 into account ###        
if      isPy2() == True:
        ### python version < 3 ###
        #using the types library for checking for built-in types is (just) python 2(.7) style
        from types            import FunctionType   as Types_FunctionType
        from types            import TupleType      as Types_TupleType
        from types            import NoneType       as Types_NoneType    
        from types            import StringTypes    as Types_StringTypes
        from types            import UnicodeType    as Types_UnicodeType
        
else:
        ### python version >= 3 ###
        def function(): 
            pass                                                                                                       # pragma: no cover
        Types_FunctionType = (type(function), Functools_partial)
        Types_TupleType    = tuple
        Types_NoneType     = None
        Types_StringTypes  = str
        Types_UnicodeType  = str
        xrange             = range
        long               = int
        
        from functools import reduce


#####################################################################
# supported operators tuples (for 'ConditionFunction' resp. 'elem') #
#####################################################################
unaryElemOperatorsT  = ( "abs", "invert", "neg"                                                   )
                     
binaryElemOperatorsT = ( "lt", "le", "eq", "ge", "gt", "ne", "add", "sub", "mul", "truediv",      \
                         "floordiv", "mod", "pow", "concat", "lshift", "rshift", "xor"            )
                         
elemRightOperatorsT  = ( "radd", "rsub", "rmul", "rtruediv", "rfloordiv", "rmod", "rdivmod",      \
                         "rpow", "rlshift", "rrshift", "rxor"                                     )
                     
#'div' just exists in Python 2.*
if      isPy2() == True:
        unaryElemOperatorsT  += ("repeat",)
        binaryElemOperatorsT += ("div",)
        elemRightOperatorsT  += ("rdiv",)

for operatorS in (unaryElemOperatorsT + binaryElemOperatorsT):
    exec("from operator import {0} as Operator_{0}".format(operatorS))

del operatorS     
               
           
#####################
# exception handler #  
#####################      
try:
        #if the pyadaaah library is available, use its exceptions / exception handler
        from pyadaaah import *
        
except: 
        #if the pyadaaah library is not available, use a dummy exception handler 
        #(but the 'logExceptions' decorator has a real meaning!)
        #STR - accepting (and translating) unicode characters too
        class STR(str):
            """
                 String class accepting e.g. and in particular unicodes as well; 
                 the result is a pure ascii (0-127) string, which is achieved by 
                 replacing all non-ascii characters by '?'.
            """
            
            #return the pure ascii string
            def __new__(cls, text):
                """ """   
                
                try:
                       #make a str out of text - if not already one (resp. an unicode)
                       if    isinstance(text, Types_StringTypes):
                             textS = text
                       else:
                             textS = str(text)
                      
                       #make a unicode out of textS - if not already one
                       if not isinstance(textS, Types_UnicodeType):
                          textS = textS.decode("ascii", "replace")
                
                       #unicode is str in python 3 - but not in python 2
                       #in python 2: encode back to str
                       if isPy2() == True:
                          #replace non-ascii characters by '?'
                          textS = textS.encode("ascii", "replace")
                          
                       #return
                       return textS
                      
                except BaseException as ee:
                       return "Error in STR: %s!" % str(ee)
                       
               
               
        #dummy exception handler
        class ExceptionHandler(object):
              """ Dummy exception handler doing nothing. """
                             
              @classmethod
              def log(cls, exception):
                  """ Does nothing. """
                  
                  pass
                  
  
    
        #exception logger - decorator for methods (only !)
        def logExceptions(method, logger=ExceptionHandler):
            """ Method wrapper for exception logging (decorator). """
        
            def decorator(self, *params, **paramDict):
                try:   
                        return method(self, *params, **paramDict)              
                        
                except  BaseException as error: 
                        #get class-s name - in a safe manner
                        clsNameS = "no class"
                        if hasattr(self, "__class__"):
                           if hasattr(self.__class__, "__name__"):
                              clsNameS = self.__class__.__name__
                        
                        #get method name - in a safe manner
                        methodNameS = "no method"
                        if hasattr(method, "__name__"):
                           methodNameS = method.__name__
                        
                        #create message - in a safe manner
                        try:
                                errMsgS = "Error in %s.%s: %s" % (clsNameS, methodNameS, STR(error))
                        except:
                                errMsgS = "automatic exception message creation failed"
                                
                        #enhance readability / beauty
                        errMsgS = errMsgS.rstrip() + Os_linesep + Os_linesep
                        
                        #log error message
                        logger.log( type(error)(errMsgS) )
                        
                        #re-raise exception
                        raise type(error)(errMsgS)
                        
            #return new (decorator) method
            return decorator
            
            
        #as the dummy logger does nothing, muting means 'doing nothing' too
        def muteLogging(method, logger=ExceptionHandler):
            """ Decorator - adding nothing to each method decorated. """
            
            def decorator(self, *params, **paramDict):
                """ This wrapper does not add any functionality. """
                
                #call method
                retVal = method(self, *params, **paramDict)
                
                #return return value of method
                return retVal
                
            #return new (decorator) method
            return decorator    



#EnhaaancedLists version
__version__ = 0.9
def getVersion():
    global __version__
    return __version__
    


##################################################
# elem term - condition (partial) function class #
############# ####################################
class ConditionFunction(Functools_partial):
      """
          --- still UNDER CONSTRUCTION ---
          
          The class 'ConditionFunction' is the basic unit of condition terms 
          - in particular those using the 'elem' term / alias / intance. Said 
          'elem' is defined in the following way:
          
          elem = ConditionFunction(lambda x: x)
          
          'ConditionFunction' is a function CLASS, whose operator methods 
          have been overloaded to each return a new ConditionFunction instance, 
          which then provides resp. keeps ready the functionality belonging 
          to the operator chosen resp. applied (by calling said methods) - 
          as a partial function; that means: 
          
          by applying an operator on a 'ConditionFunction' instance one
          constructs a new 'ConditionFunction' instance with the functionality
          of said operator - on which then again another operator can be
          applied to construct another function comprising the functionality
          of both operators to be applied sequentially - and so on.
          
          In particular, the operator methods for getting an attribute ('.') 
          and for getting an item ('[]') have been overloaded this way, as 
          well as the comparison operator methods. 
          
          Furthermore the bitwise 'or' and 'and' operator methods are abused 
          to provide a logical 'or' and 'and' too.
          
          Further operators yet already taken into account can be found in 
          'unaryElemOperatorsT', 'binaryElemOperatorsT' and 
          'elemRightOperatorsT' of the enhaaancedLists module.
          
          
          In Short:
          =========
          
          this condition resp. function can be 'extended' by 
          using (said) operators on it - which then leads to an(other) 
          (extended) condition resp. function resp. ConditionFunction.
          
          
          Examples:
          =========
          
          selector = (elem['a'] > 5) & (elem['b'] < 5)
          #creates a 'ConditionFunction' taking one parameter (an 'element')
          
          selector( {'a':6, 'b':4} ) ==> True
          selector( {'a':4, 'b':6} ) ==> False
          
          operator = (elem['a'] + elem['b']) * 2
          #creates a 'ConditionFunction' taking one parameter (an 'element')
          
          operator( {'a':6, 'b':4} ) ==> 20
          
          
          NOTE:
          ====
          
          THAT THE 'ELEM' TERM MECHANISM IS LIMITED YET! 
          
          It just is a short convenience notation, which can be used to 
          enhance the readability of some SIMPLE conditions for element 
          selection or of some SIMPLE operations on elements.
          
          Some methods of EnhList accept ConditionFunction-s as parameter-s. 
          For those, you either can use the ConditionFunction resp. 'term'
          mechanism, or a function, alike a lambda.
      """
       
      #generate unary operator methods
      for operatorS in unaryElemOperatorsT:
          exec( """@logExceptions
def __{0}__(self):
    ' overloaded unary operator method '
    return ConditionFunction( lambda x: Operator_{0}(self(x)) )
                """.format(operatorS))
                
                
      #generate binary operator methods
      for operatorS in binaryElemOperatorsT:
          exec( """@logExceptions
def __{0}__(self, ohs):
    ' overloaded binary operator method '
    if    isinstance(ohs, Functools_partial):
          return ConditionFunction( lambda x: Operator_{0}(self(x), ohs(x)) )
    else:
          return ConditionFunction( lambda x: Operator_{0}(self(x), ohs) )
                """.format(operatorS))
                
                
      #generate right operator methods
      for operatorS in elemRightOperatorsT:
          exec( """@logExceptions
def __{0}__(self, ohs):
    ' overloaded right operator method '
    if    isinstance(ohs, Functools_partial):
          return ConditionFunction( lambda x: Operator_{1}(ohs(x), self(x)) )
    else:
          return ConditionFunction( lambda x: Operator_{1}(ohs, self(x)) )
                """.format(operatorS, operatorS[1:]))

      del operatorS


      #called if the 'bitwise and' operator '&' is used on a ConditionFunction instance
      @logExceptions
      def __and__(self, ohs):
          """ As there is no hook for the 'logical and' operator, 
              the 'bitwise and' is 'abused' instead.               """
      
          if    isinstance(ohs, Functools_partial):
                return ConditionFunction( lambda x: (self(x) and ohs(x)) )    
          else:
                return ConditionFunction( lambda x: (self(x) and ohs) )
          
          
      #called if the 'bitwise or' operator '|' is used on self
      @logExceptions
      def __or__(self, ohs):
          """ As there is no hook for the 'logical or' operator, 
              the 'bitwise or' is 'abused' instead.                """
       
          if    isinstance(ohs, Functools_partial):
                return ConditionFunction( lambda x: (self(x) or ohs(x)) ) 
          else:
                return ConditionFunction( lambda x: (self(x) or ohs) )
                
                
      #method called by ".nameS"
      @logExceptions
      def __getattribute__(self, nameS):
          """ overloaded get attribute method """
          
          #do not meddle with resp. change the classes standard attributes (accesses)
          if    not nameS.startswith("__"): 
                return ConditionFunction( Operator_attrgetter(nameS) )
          else:
                return Functools_partial.__getattribute__(self, nameS)
          
          
      #method called by "[nameS]"
      @logExceptions
      def __getitem__(self, keyO):
          """ overloaded get item method """
          
          return ConditionFunction( Operator_itemgetter(keyO) )   
      
      
### short elem alias ###
elem = ConditionFunction(lambda x: x)


#self test method
def _elemSelftest():
    """ Does some tests using the 'elem' notation. """
    
    print ( "Testing 'elem'..." )
    
    #lower than comparison operator
    fct = elem < 5
    assert fct(4) == True
    assert fct(6) == False  
    
    #lower or equal comparison operator
    fct = elem <= 5
    assert fct(5) == True
    assert fct(6) == False
    
    #equal comparison operator
    fct = elem == 5
    assert fct(5) == True
    assert fct(6) == False
    
    #greater or equal comparison operator
    fct = elem >= 5
    assert fct(6) == True
    assert fct(4) == False
    
    #greater comparison operator
    fct = elem > 5
    assert fct(6) == True
    assert fct(5) == False
    
    #not equal comparison operator
    fct = elem != 5
    assert fct(4) == True
    assert fct(5) == False
    
    #add operator
    fct = 1 < elem + 1
    assert fct(1) == True
    assert fct(0) == False
    
    #subtract operator
    fct = 1 < elem - 1
    assert fct(3) == True
    assert fct(2) == False
    
    #multiply operator
    fct = 1 < elem * 2
    assert fct(1) == True
    assert fct(0) == False
    
    #divide operator
    fct = 1 < elem / 2
    assert fct(4.0) == True
    assert fct(2.0) == False
    
    #int divide operator
    fct = elem // 2 >= 1
    assert fct(4) == True
    assert fct(1) == False
    
    #modulo operator
    fct = elem % 2 == elem % 4
    assert fct(4) == True
    assert fct(2) == False
    
    #power operator
    fct = elem ** 2 != 16
    assert fct(3) == True
    assert fct(4) == False
    
    ### unary operators ###
    assert abs(elem)(-1.23) == 1.23
    assert (~elem)(255)     == -256
    assert (-elem)(1.23)    == -1.23
    assert (2*elem)("abc")  == "abcabc"
    assert (elem*2)("abc")  == "abcabc"
    
    ### binary operators ###
    assert (elem < 5)(4)    == True
    assert (elem < 5)(5)    == False
    assert (5 > elem)(4)    == True
    assert (5 > elem)(5)    == False
    
    assert (elem <= 5)(4)    == True
    assert (elem <= 5)(6)    == False
    assert (5 >= elem)(4)    == True
    assert (5 >= elem)(6)    == False
    
    assert (elem == 5)(5)    == True
    assert (elem == 5)(4)    == False
    
    assert (elem > 5)(4)     == False
    assert (elem > 5)(6)     == True
    assert (5 < elem)(4)     == False
    assert (5 < elem)(6)     == True
    
    assert (elem >= 5)(4)    == False
    assert (elem >= 5)(6)    == True
    assert (5 <= elem)(4)    == False
    assert (5 <= elem)(6)    == True
    
    assert (elem != 5)(5)    == False
    assert (elem != 5)(4)    == True

    assert (elem - 2)(5)     == 3
    assert (2 - elem)(5)     == -3
    
    assert (elem + 2)(5)     == 7
    assert (2 + elem)(5)     == 7

    assert (elem * 2)(5)     == 10
    assert (2 * elem)(5)     == 10

    assert (elem / 2.0)(5)   == 2.5
    assert (1.0 / elem)(5)   == 0.2
    
    assert (elem // 2)(11)   == 5
    assert (11 // elem)(2)   == 5
    
    assert (elem % 8)(11)    == 3
    assert (11 % elem)(8)    == 3
    
    assert (elem ** 2)(3)    == 9
    assert (3 ** elem)(2)    == 9
    
    assert (elem + "cd")("abc") == "abccd"
    assert ("abc" + elem)("cd") == "abccd"
    
    assert (elem << 2)(1)    == 4
    assert (elem >> 2)(4)    == 1
    
    assert (elem ^ 3)(5)    == 6
    assert (3 ^ elem)(5)    == 6

    print ("...'elem' tested successfully!")   



#single
class Single(object):
      """ 
          Just a helper class for EnhList.
          Some methods of EnhList accept that as a parameter.
      """
      pass
single = Single()

#several
class Several(object):
      """ 
          Just a helper class for EnhList.
          Some methods of EnhList accept that as a parameter.
      """
      pass
several = Several()

#debug
class Debug(object): 
      """ 
          Just a helper class for EnhList.
          
          Allows printing out all incoming (just via 'push')
          and outgoing (just via 'pop') elements of an 'EnhList'
          whose debugging option has been switched on using
          'toggleDebugMode(True)'.
      """
      
      #print method
      @classmethod
      def printt(cls, headerS, obj):
          """ 
               A hook method for printing an incoming/outgoing object
               in debug mode.
          """
          
          print (headerS + str(obj))
          Sys_stdout.flush()
          Sys_stderr.flush()
          
          
          
#(just) a helper class for TypedList
class TypeMismatch(BaseException):
      """
          Raised when doc TYPE checking leads to an error.
      """
      
      pass



#(just) a helper class for EnhList - list with an automatic type check / enforcement
class TypedList(list):
      """ 
          Can either be used (just) as a normal 'list' (if NO 'elemTypesT' keyword parameter 
          is given) or as a typed list (if an 'elemTypesT' keyword parameter is given) - which 
          means, that assigning elements of types, which are not in said 'elemTypesT' tuple, 
          leads to exceptions.
          
          Some premade typed list classes are provided:
          
          DecimalList            #inherited from EnhList (which inherits from TypedList)
          DictList
          FloatList
          IntList
          ListList
          LupleList              #elements can be of type list or tuple
          NumberList             #elements can be of type int, float and decimal.Decimal
          SetList
          StrList
          TupleList
          
          DecimalSecList         #inherited from SecList (which inherits from EnhList)
          DictSecList
          FloatSecList
          IntSecList
          ListSecList
          LupleSecList           #elements can be of type list or tuple
          NumberSecList          #elements can be of type int, float and decimal.Decimal
          SetSecList
          StrSecList
          TupleSecList
      """
      
      _elemTypesT  = None
      
      
      #constructor
      @logExceptions
      def __init__(self, *params, **paramDict):
          """
              Accepts all positional (non-keyword) parameters, which the parent class 'list' accepts.
              
              The only keyword parameter taken into account - if provided - is 'elemTypesT'.
              It then must be a 'tuple' of types, which 'TypedList' should accept for its
              elements - elements of another type then are not accepted (an exception is raised then).
              
              If said 'elemTypesT' parameter is not provided, 'TypedList' just is a normal (untyped)
              'list'.
          """
                   
          ###ignore keys from paramDict - but the parameter 'elemTypesT' ###
          if    'elemTypesT' in paramDict.keys():
                #init
                self._elemTypesT = paramDict['elemTypesT']
                
                #check elem types
                if self._elemTypesT != None:
                   if not isinstance(self._elemTypesT, tuple)                   or \
                      not all( map(lambda x: type(x) == type, self._elemTypesT)    ):
                      raise Exception("Parameter 'elemTypesT' must be a tuple of types!")
                
          else:
                self._elemTypesT = None
                
          #call parents constructor
          list.__init__(self, *params)
          
          #do type checking, if types are given in 'self._elemTypesT'
          if self._elemTypesT != None:
             ### do type checking ###
             if not all([ isinstance(el, self._elemTypesT) for el in self ]):
                raise TypeMismatch( "all elements of 'self' must be of any type of %s (not '%s')!" % \
                                    (list(self._elemTypesT), self)                                   )


      #set item
      @logExceptions
      def __setitem__(self, index, value):
          """ 
              If 'self._elemTypesT' is a tuple of types, the elements of 'self' will only
              be allowed to be of said types ('self' then is a type checked list). If, 
              on the other hand, 'self._elemTypesT' is 'None' there will be no such 
              restriction for the elements of 'self' (which then just is a 'normal' 'list').
              
              In Python 3 this method also is called instead of '__setslice__' - the parameter
              'index' then is of type 'slice' and 'value' is an iterable.
          """         

          #do type checking, if types are given in 'self._elemTypesT'
          if self._elemTypesT != None:
             ### do type checking ###
            
             #check whether 'set item' or 'set slice' is to be done
             if    isinstance(index, int):
                   ### python 2 & 3 __setitem__ (set single value) - check parameter 'value' ###
                   if not isinstance(value, self._elemTypesT):
                      raise TypeMismatch( "parameter 'value' must be of any type in %s (not '%s' of %s)!" % \
                                          (self._elemTypesT, value, type(value))                            )

             elif  isinstance(index, slice):
                   ### python 3 __setslice__ (set slice of several values) replacement ###
                   if not all([ isinstance(el, self._elemTypesT) for el in value ]):
                      raise TypeMismatch( "(setslice replacement) all elements of parameter 'value' " \
                                          "must be of any type of %s!" % list(self._elemTypesT)       )
             
          #call parents set item method
          return list.__setitem__(self, index, value)
          
          
      #insert item
      @logExceptions
      def insert(self, index, value):
          """ 
              If 'self._elemTypesT' is a tuple of types, the elements of 'self' will only
              be allowed to be of said types ('self' then is a type checked list). If, 
              on the other hand, 'self._elemTypesT' is 'None' there will be no such 
              restriction for the elements of 'self' (which then just is a 'normal' 'list').
          """         

          #do type checking, if types are given in 'self._elemTypesT'
          if self._elemTypesT != None:
             ### do type checking ###
            
             #check type of 'value'
             if not isinstance(value, self._elemTypesT):
                raise TypeMismatch( "parameter 'value' must be of any type in %s (not '%s' of %s)!" % \
                                    (self._elemTypesT, value, type(value))                            )
                                    
          #call parents append method
          return list.insert(self, index, value)
          
          
      #append item
      @logExceptions
      def append(self, value):
          """ 
              If 'self._elemTypesT' is a tuple of types, the elements of 'self' will only
              be allowed to be of said types ('self' then is a type checked list). If, 
              on the other hand, 'self._elemTypesT' is 'None' there will be no such 
              restriction for the elements of 'self' (which then just is a 'normal' 'list').
          """         

          #do type checking, if types are given in 'self._elemTypesT'
          if self._elemTypesT != None:
             ### do type checking ###
            
             #check type of 'value'
             if not isinstance(value, self._elemTypesT):
                raise TypeMismatch( "parameter 'value' must be of any type in %s (not '%s' of %s)!" % \
                                    (self._elemTypesT, value, type(value))                            )
                                    
          #call parents append method
          return list.append(self, value)
          
          
      #set slice
      @logExceptions
      def __setslice__(self, lowerIndexI, upperIndexI, values):
          """
              If 'self._elemTypesT' is a tuple of types, the elements of 'self' will only
              be allowed to be of said types ('self' then is a type checked list). If, 
              on the other hand, 'self._elemTypesT' is 'None' there will be no such 
              restriction for the elements of 'self' (which then just is a 'normal' 'list').
              
              Note that Python 3 does not use 'self.__setslice__' anymore - it uses
              'self.__setitem__' with a 'slice' index type instead.
          """

          #do type checking, if types are given in 'self._elemTypesT'
          if self._elemTypesT != None:
             ### do type checking ###
                    
             #check parameter 'values'
             if not all([ isinstance(el, self._elemTypesT) for el in values ]):
                raise TypeMismatch( "all elements of parameter 'values' must be of any type of %s!" % \
                                    list(self._elemTypesT)                                            )
                
          #call parents set slice method
          return list.__setslice__(self, lowerIndexI, upperIndexI, values)
          
          
      #extend
      @logExceptions
      def extend(self, values):
          """
              If 'self._elemTypesT' is a tuple of types, the elements of 'self' will only
              be allowed to be of said types ('self' then is a type checked list). If, 
              on the other hand, 'self._elemTypesT' is 'None' there will be no such 
              restriction for the elements of 'self' (which then just is a 'normal' 'list').
          """

          #do type checking, if types are given in 'self._elemTypesT'
          if self._elemTypesT != None:
             ### do type checking ###
                    
             #check parameter 'values'
             if not all([ isinstance(el, self._elemTypesT) for el in values ]):
                raise TypeMismatch( "all elements of parameter 'values' must be of any type of %s!" % \
                                    list(self._elemTypesT)                                            )
                
          #call parents extend method
          return list.extend(self, values)
          
          
      #add
      @logExceptions
      def __add__(self, ohs):
          """
              If 'self._elemTypesT' is a tuple of types, the elements of 'self' will only
              be allowed to be of said types ('self' then is a type checked list). If, 
              on the other hand, 'self._elemTypesT' is 'None' there will be no such 
              restriction for the elements of 'self' (which then just is a 'normal' 'list').
          """
          
          #ensure, that ohs is a list
          if not isinstance(ohs, list):
             raise Exception( "just a list can be added to 'self' (not a %s)!" % type(ohs) )

          #do type checking, if types are given in 'self._elemTypesT'
          if self._elemTypesT != None:
             ### do type checking ###
                    
             #check parameter 'values'
             if not all([ isinstance(el, self._elemTypesT) for el in ohs ]):
                raise TypeMismatch( "all elements of parameter 'ohs' must be of any type of %s!" % \
                                    list(self._elemTypesT)                                         )
                
          #call parents extend method
          return TypedList( list.__add__(self, ohs), elemTypesT=self._elemTypesT )
          
          
      #iadd
      @logExceptions
      def __iadd__(self, ohs):
          """
              If 'self._elemTypesT' is a tuple of types, the elements of 'self' will only
              be allowed to be of said types ('self' then is a type checked list). If, 
              on the other hand, 'self._elemTypesT' is 'None' there will be no such 
              restriction for the elements of 'self' (which then just is a 'normal' 'list').
          """
          
          #ensure, that ohs is a list
          if not isinstance(ohs, (list, tuple)):
             raise Exception( "just a list or tuple can be added to 'self' (not a %s)!" % type(ohs) )

          #do type checking, if types are given in 'self._elemTypesT'
          if self._elemTypesT != None:
             ### do type checking ###
                    
             #check parameter 'values'
             if not all([ isinstance(el, self._elemTypesT) for el in ohs ]):
                raise TypeMismatch( "all elements of parameter 'ohs' must be of any type of %s!" % \
                                    list(self._elemTypesT)                                         )
                
          #call parents extend method
          return list.__iadd__(self, ohs)
          
          
          
      #method testing self
      @classmethod
      def _selftest(cls):            
          """
              If no exception is raised during the execution of this method 
              the TypedList class behaves as expected.
              
              It e.g. can be used to check the integrity after modifications
              or to check the compatibility with specific python versions.
              
              Have a look into the methods called in this method for examples,
              how TypedList can be used.
          """
          
          print ( "Testing TypedList..." )

          ### as normal list ###
          typedL = TypedList([1,3,5,7,9,11])
          assert typedL == [1,3,5,7,9,11]
          
          typedL[1]      = 4
          assert typedL == [1,4,5,7,9,11]
          
          typedL[3:5]    = [6,8]
          assert typedL == [1,4,5,6,8,11]
          
          typedL[2]      = "a"
          typedL[4:6]    = ["b", "c"]
          assert typedL == [1,4,"a",6,"b","c"]
          
          typedL.append(7)
          assert typedL == [1,4,"a",6,"b","c",7]
          
          typedL.extend([9,"z"])
          assert typedL == [1,4,"a",6,"b","c",7,9,"z"]
          
          typedL.insert(3, 111)
          assert typedL == [1,4,"a", 111,6,"b","c",7,9,"z"]
          
          typedL         = typedL + [11, 22, 33]
          assert typedL == [1,4,"a", 111,6,"b","c",7,9,"z",11,22,33]
          assert isinstance(typedL, TypedList)
          
          typedL        += [12,34,56]
          assert typedL == [1,4,"a", 111,6,"b","c",7,9,"z",11,22,33,12,34,56]
          assert isinstance(typedL, TypedList)
          
          ### as typed list ###
          typedL = TypedList([1,3,5,7,9,11], elemTypesT=(int, float))
          assert typedL == [1,3,5,7,9,11]
          
          typedL[1]      = 4
          assert typedL == [1,4,5,7,9,11]
          
          typedL[1]      = 4.123
          assert typedL == [1,4.123,5,7,9,11]          
          
          typedL[3:5]    = [6,8.123]
          assert typedL == [1,4.123,5,6,8.123,11]
          
          typedL.append(7)
          assert typedL == [1,4.123,5,6,8.123,11,7]
          
          typedL.extend([9,11.1])
          assert typedL == [1,4.123,5,6,8.123,11,7,9,11.1]
          
          typedL.insert(3, 11.2)
          assert typedL == [1,4.123,5,11.2,6,8.123,11,7,9,11.1]
          
          typedL         = typedL + [11, 22, 33]
          assert typedL == [1,4.123,5,11.2,6,8.123,11,7,9,11.1,11,22,33]
          assert isinstance(typedL, TypedList)
          
          typedL        += [12,34,56]
          assert typedL == [1,4.123,5,11.2,6,8.123,11,7,9,11.1,11,22,33,12,34,56]
          assert isinstance(typedL, TypedList)          
          
          ### check type checking ###
          try:
                  typedL[2]      = "a"
                  assert False                                                                                         # pragma: no cover
                  
          except  TypeMismatch:
                  pass
                
          try:
                  typedL[4:6]    = [111, "c"]
                  assert False                                                                                         # pragma: no cover
                  
          except  TypeMismatch:
                  pass
                
          try:
                  typedL[4:6]    = ["b", 222]
                  assert False                                                                                         # pragma: no cover
                  
          except  TypeMismatch:
                  pass
                
          assert typedL == [1,4.123,5,11.2,6,8.123,11,7,9,11.1,11,22,33,12,34,56]
          
          try:
                  typedL = TypedList([1,3,5,"a",9,11], elemTypesT=(int, float))
                  assert False                                                                                         # pragma: no cover
                  
          except  TypeMismatch:
                  pass
                
          #append, extend, insert and add/iadd
          typedL = TypedList([1,3,5], elemTypesT=(int, float))
          
          try:
                  typedL.append("abc")
                  assert False                                                                                         # pragma: no cover
                  
          except  TypeMismatch:
                  pass

          try:
                  typedL.extend(["abc", "def"])
                  assert False                                                                                         # pragma: no cover
                  
          except  TypeMismatch:
                  pass
                
          try:
                  typedL.insert(1, "abc")
                  assert False                                                                                         # pragma: no cover
                  
          except  TypeMismatch:
                  pass
                
          try:
                  typedL + ["abc", "def"]
                  assert False                                                                                         # pragma: no cover
                  
          except  TypeMismatch:
                  pass
                
          try:
                  typedL += ["abc", "def"]
                  assert False                                                                                         # pragma: no cover
                  
          except  TypeMismatch:
                  pass
          
          print ( "...TypedList tested successfully." )



#######################
# Enhanced List Class #
#######################
class EnhList(TypedList):
      """ 
          List with extended / enhanced IN-PLACE capabilities, also inheriting type
          checking means from the class 'TypedList'.
          
          Together with the 'elem' term, some of its 
          methods (also) allow using a NEW OPERATOR NOTATION, closely 
          resembling mathematical conditions / terms.
          
          Note that '&' and '|' are 'abused' as 'logical and / or' in this
          context (and NOT as bitwise oprators!).
          
          examples for said ADDITIONAL capabilities (standard list operations work too):
          
          
          #convert a parameter list to an enhanced list 
          eL = EnhList(1,3,5,7)                                       #eL: [1,3,5,7]
          
          #push single as well as multiple elements into the list
          eL.push(9)                                  ==> None        #eL: [1,3,5,7,9]
          eL.push(11,13,15)                           ==> None        #eL: [1,3,5,7,9,11,13,15]
          
          #pop - note that push/pop implements a FIFO - in contrast to the standard list
          eL.pop()                                    ==> 1           #eL: [3,5,7,9,11,13,15]
          eL.pop( (elem > 3) & (elem < 11), single )  ==> 5           #eL: [3,7,9,11,13,15]
          eL.pop( (elem > 3) & (elem < 11)         )  ==> [7,9]       #eL: [3,11,13,15]
          
          #extend - 
          eL.extend( [7,8,9] )                        ==> None        #eL: [3,11,13,15,7,8,9]
          eL.extend( [4,5,6], reverse=True )          ==> None        #eL: [4,5,6,3,11,13,15,7,8,9]
          
          #get items from list
          eL[ elem >= 10         ]                    ==> [11,13,15]  #eL: unchanged
          eL[ elem >= 10, single ]                    ==> 11          #eL: unchanged
          eL[ elem <  3,  single ]                    ==> None        #eL: unchanged
          
          #check whether list contains items
          ( elem <  3 ) in eL                         ==> False       #eL: unchanged
          ( elem >= 3 ) in eL                         ==> True        #eL: unchanged
          
          #set items in list                                          
          eL = EnhList(4,5,6,3,11,13,15,7,8,9)                        #eL: [4,5,6,3,11,13,15,7,8,9]
          eL[ elem % 2 == 1]              = elem // 2 ==> None        #eL: [4,2,6,1,5,6,7,3,8,4]
          eL[ (elem == 6) | (elem == 8) ] = 0         ==> None        #eL: [4,2,0,1,5,0,7,3,0,4]
          
          #delete items from list
          eL = EnhList(4,5,6,3,11,13,15,7,8,9)                        #eL: [4,5,6,3,11,13,15,7,8,9]
          del eL[ elem < 12, single ]                 ==> ---         #eL: [5,6,3,11,13,15,7,8,9]
          del eL[ elem > 12         ]                 ==> ---         #eL: [5,6,3,11,7,8,9]
          
          eL = EnhList(1,3,5,7)                                       #eL: [1,3,5,7]
          #check whether all elements meet a condition
          eL.areAll( elem % 2 == 1 )                  ==> True
          eL.areAll( elem     >= 3 )                  ==> False
          
          #map function on elements / work with items of elements
          #map replaces elements, which are mapped, by the mapping result
          eL.mapIf( lambda x: dict(a=x) )                          
                                                      ==> None        #eL: [{'a':1},{'a':3},{'a':5},{'a':7}]
          eL.mapIf( lambda x: x['a'] + 1, elem['a'] > 3)           
                                                      ==> None        #eL: [{'a':1},{'a':3},6,8]
            
          #apply map function on elements / work on items of elements                                          
          #apply map does not replace elements; it modifies elements, which are apply mapped, instead
          eL = EnhList([3],[5],[7])                                             #eL: [[3],    [5],       [7]      ]
          eL.applyMapIf( lambda x: list.append(x, 22) )              ==> None   #eL: [[3,22], [5,22],    [7,22]   ]
          eL.applyMapIf( lambda x: list.append(x, 33), elem[0] > 4 ) ==> None   #eL: [[3,22], [5,22,33], [7,22,33]]
          
          #get min, max, avg or median of a selected property
          eL = EnhList([3,8],[5,6],[7,4])                             #eL: [[3,8],[5,6],[7,4]]
          eL.min(    elem[0] )                        ==> 3           #eL: [[3,8],[5,6],[7,4]]
          eL.max(    elem[1] )                        ==> 8           #eL: [[3,8],[5,6],[7,4]]
          eL.avg(    elem[0] )                        ==> 5.0         #eL: [[3,8],[5,6],[7,4]]
          eL.median( elem[1] )                        ==> 6.0         #eL: [[3,8],[5,6],[7,4]]
          eL.sum(    elem[0] )                        ==> 15          #eL: [[3,8],[5,6],[7,4]]
          
          #work with attributes of elements
          eL = EnhList([{'a':1},{'a':3},6,8])                         #eL: [{'a':1},{'a':3},6,8]
          class Attr(object):
                def __init__(self, value):
                    self.a = value
                def __repr__(self):
                    return ".a=%s" % self.a
          eL.mapIf( lambda x: Attr(x), lambda x: type(x) ==  int ) 
                                                      ==> None        #eL: [{'a':1},{'a':3},.a=6,.a=8]
                                                      
          #create a list, whose elements just can be of given types (a typed list)
          eL = EnhList(1,3,5,7, elemTypesT=(int, float))              #eL: [1,3,5,7]
          eL.append(1.23)                             ==> None        #eL: [1,3,5,7,1.23]
          eL.append("a")                              ==> TypeMismatch exception
          
          #for the aforementioned use case, there also are some premade typed lists
          eL = NumberList(1,3,5,7)                                    #eL: [1,3,5,7]
          eL.append(1.23)                             ==> None        #eL: [1,3,5,7,1.23]
          eL.append("a")                              ==> TypeMismatch exception
          
          Said premade typed list classes are:
          
          DecimalList            #inherited from EnhList
          DictList
          FloatList
          IntList
          ListList
          LupleList              #elements can be of type list or tuple
          NumberList             #elements can be of type int, float and decimal.Decimal
          SetList
          StrList
          TupleList
          
          DecimalSecList         #inherited from SecList
          DictSecList
          FloatSecList
          IntSecList
          ListSecList
          LupleSecList           #elements can be of type list or tuple
          NumberSecList          #elements can be of type int, float and decimal.Decimal
          SetSecList
          StrSecList
          TupleSecList
                
          More examples can be found in the source code of the selftest function
          of the module and the methods called from there - in particular in 
          'SecList._selftest'.
          
          Please also take the doc/help-texts of each revised method into account too.
          
          Also note, that 'elem' just is an alias defined as follows:
          
          elem = ConditionFunction(lambda x: x)
          
          So that more informations about 'elem' also can be found in the doc/help-text
          belonging to the class 'ConditionFunction', which, by the way, is inherited from
          functools.partial.
          
          Additional or modified API methods (compared to 'list'):
          ========================================================
          
          toggleDebugMode(debugModeB=None, listNameS=None) --> None                         #toggle debug mode for 'push' and 'pop'.
          extend(*params, **paramDict)                     --> None                         #this method is the 'list.extend' augmented by an additional keyword parameter 'reverse', which allows (if 'True') to extend at the beginning too.
          push(*params)                                    --> None                         #combines 'list.append' with 'list.extend' to allow single as well as several parameters / elements (to be appended - at the end).
          pop(selector=0, multitude=several)               --> element or list of elements  #'list.pop' with comprehensively extended functionality - see examples.
          areAll(conditionFct)                             --> bool                         #returns 'True' if conditionFct returns 'True' for (applied on) all elements, 'False' otherwise.
          mapIf(*params)                                   --> None                         #replaces elements meeting the condition function (second positional parameter - if any) by the mapping function (first positional parameter) applied to said elements.
          applyMapIf(*params)                              --> None                         #(just) applies the mapping function (first positional parameter) to all elements meeting the condition function (second positional parameter - if any). Elements are NOT replaced (as with 'mapIf').
          min(propertySelFct=elem)                         --> minimum                      #maps the property selector (partial) function 'propertySelFct' to all elements and returns the minimum of the resulting value list.
          max(propertySelFct=elem)                         --> maximum                      #maps the property selector (partial) function 'propertySelFct' to all elements and returns the maximum of the resulting value list.
          sum(propertySelFct=elem)                         --> sum                          #maps the property selector (partial) function 'propertySelFct' to all elements and returns the sum of the resulting value list.
          avg(propertySelFct=elem)                         --> average                      #maps the property selector (partial) function 'propertySelFct' to all elements and returns the average of the resulting value list.
          median(propertySelFct=elem)                      --> median                       #maps the property selector (partial) function 'propertySelFct' to all elements and returns the median of the resulting value list.
      """
      
      _listNameS  = None               #the name of this list print-ed in debug mode (see line below)
      _debugModeB = None               #whether debug mode (some additional print-s) is activated or not
      
      
      #initialisation
      @logExceptions
      def __init__(self, *params, **paramDict):
          """
               If several positional parameters 'params' are given, they are taken
               as the initial elements of the (enhanced) list.
               
               Otherwise, 'params' (just) is forwarded to the __init__ method
               of the parent 'list' class as is.
               
               The only keyword parameter taken into account, if given, is
               'elemTypesT' - which either can be 'None' (no type checking) or
               a tuple of allowed types (a TypeMismatch exception is raised, if
               an element is set to a type other than said types).
          """
          
          #just take "elemTypesT" keyword parameter into account - if given
          elemTypesT = None
          if "elemTypesT" in paramDict.keys():
             elemTypesT = paramDict["elemTypesT"]          

          #call the __init__ of the parent class according to the number of given positional parameters
          if    len(params) <= 1:
                #no or one parameter ==> use it as parameter for __init__ of the parent class
                TypedList.__init__(self, *params, elemTypesT=elemTypesT)
                
          else:
                #several parameters ==> use it as initial elements of the (enhanced resp typed) list
                TypedList.__init__(self,  params, elemTypesT=elemTypesT)
                
          #init name and debug mode
          self._listNameS  = ""          
          self._debugModeB = False
                
                
      #method testing __init__
      @classmethod
      @muteLogging
      def _initSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__init__..." )
          
          #no parameter
          assert EnhList() == []
          assert EnhList(elemTypesT=(int, float)) == []

          #one -non iterable- parameter  
          try:        
                  assert EnhList(1)
                  assert False                                                                                         # pragma: no cover
          except  TypeError:
                  pass
          try:        
                  assert EnhList(1, elemTypesT=(int, float))
                  assert False                                                                                         # pragma: no cover
          except  TypeError:
                  pass
                
          #one -iterable- parameter
          assert EnhList([1,3,5,7]) == [1,3,5,7]
          assert EnhList((1,3,5,7)) == [1,3,5,7]
          assert EnhList([1,3,5,7], elemTypesT=(int, float)) == [1,3,5,7]
          assert EnhList((1,3,5,7), elemTypesT=(int, float)) == [1,3,5,7]
          try:        
                  assert EnhList([1,"a",5,7], elemTypesT=(int, float))
                  assert False                                                                                         # pragma: no cover
          except  TypeMismatch:
                  pass
          
          #several parameters
          assert EnhList(1,3,5,7) == [1,3,5,7]
          assert EnhList(1,3,5,7, elemTypesT=(int, float)) == [1,3,5,7]
          try:        
                  assert EnhList(1,"a",5,7, elemTypesT=(int, float))
                  assert False                                                                                         # pragma: no cover
          except  TypeMismatch:
                  pass
          
          print ( "...EnhList.__init__ tested sucessfully!" )
          
          
      #switch debug on/off
      @logExceptions
      def toggleDebugMode(self, debugModeB=None, listNameS=None):
          """ 
              If parameter 'debugModeB' is 'None', debug mode is switched on resp. off - 
              if it was 'off' resp. 'on' before.
              
              If parameter 'debugModeB' is 'True' resp. 'False', debug mode is switched
              on resp. off (independently of what it was before).
              
              If debug mode is on, all incoming (just via 'push') and outgoing (just via
              'pop') elements are printed out using the hook method 'Debug.printt'.              
          """
          
          #init list name - if any belonging string given 
          if isinstance(listNameS, str):
             self._listNameS = listNameS
          
          #toggle debug mode                    
          if    debugModeB == None:
                if    self._debugModeB == False:
                      self._debugModeB  = True
                      print ("Debug mode toggled on for (Enh*)List with id (%d): %s" % (id(self), self._listNameS))
                      
                elif  self._debugModeB == True:
                      self._debugModeB  = False
                
                else:
                      raise Exception( "The attribute 'self._debugModeB' must either be 'True' or 'False' (not %s)!" % \
                                       self._debugModeB                                                                )
               
          elif  debugModeB in [True, False]:
                self._debugModeB = debugModeB
                
                if debugModeB == True:
                   print ("Debug mode toggled on for (Enh*)List with id (%d): %s" % (id(self), self._listNameS))
               
          else:
                raise Exception( "The parameter 'debugModeB' must either be 'None', 'True' or 'False' (not %s)!" % \
                                 debugModeB                                                                        )
                                 
          #nothing to return
          return None
          
          
      #extend at the end or the beginning
      @logExceptions          
      def extend(self, *params, **paramDict):
          """
              It accepts a non-keyword parameter of iterable type
              (resp. of a type, which can be converted to 'list')
              
              as well as the keyword parameter 'reverse', which must
              either be 'True' or 'False' (default is 'False').
              
              If 'reverse' is given and 'True', self is not extended
              at the end (which is the standard behaviour) - but at the
              beginning.
          """
          
          #handle parameter 'reverse' - whether given or not
          paramD      = paramDict.copy()
          reverseB    = False
          if "reverse" in paramD.keys():
             reverseB = paramD.pop("reverse")
             if not isinstance(reverseB, bool):
                raise Exception("The parameter 'reverse' must be of type 'bool' (not %s)!" % type(reverseB))
                
          #ensure, that no other keyword parameter is given
          if len(paramD.keys()) > 0:
             raise Exception("Unknown keyword parameter (%s)!" % paramD.keys())
                
          #ensure, that there just is a single iterable, non-keyword parameter
          if (len(params) != 1) or (not hasattr(params[0], "__iter__")):
             raise Exception("There must (exactly) be a single iterable, non-keyword parameter (not %s)!" % str(params))
                    
          #extend self
          lenI   = TypedList.__len__(self)
          retVal = TypedList.extend( self, list(params[0]) )
          if    (reverseB == True) and (lenI > 0):
                #REVERSE option is given - extend at the beginning (not the end)
                if isPy2() == True:
                      oldL   = TypedList.__getslice__(self, 0, lenI)
                      TypedList.__delslice__(self, 0, lenI)
                      
                else:
                      oldL   = TypedList.__getitem__(self, slice(0, lenI, None))
                      TypedList.__delitem__(self, slice(0, lenI, None))
                retVal = TypedList.extend( self, list(oldL) )
          
          #return None
          return retVal
          
          
      #test extend method
      @classmethod         
      def _extendSelftest(self):
          """ """          
           
          print ( "Testing EnhList.extend..." )

          #untyped mode
          firstL  = EnhList(1,3,5)
          secondL = EnhList(7,9)
          
          firstL.extend( secondL )
          assert firstL == [1,3,5,7,9]
          assert isinstance(firstL, EnhList)
          
          firstL  = EnhList(1,3,5)
          secondL = EnhList(7,9)
          
          firstL.extend( secondL, reverse=True )
          assert firstL == [7,9,1,3,5]
          assert isinstance(firstL, EnhList)
          
          #typed mode
          firstL  = EnhList(1,3,5, elemTypesT=(int,float))
          secondL = EnhList(7,9, elemTypesT=(int,float))
          
          try:        
                  firstL.extend( [11,"a",22] )
                  assert False                                                                                         # pragma: no cover
          except  TypeMismatch:
                  pass
          
          firstL.extend( secondL )
          assert firstL == [1,3,5,7,9]
          assert isinstance(firstL, EnhList)
          
          firstL  = EnhList(1,3,5, elemTypesT=(int,float))
          secondL = EnhList(7,9, elemTypesT=(int,float))
          
          try:        
                  firstL.extend( [11,"a",22], reverse=True )
                  assert False                                                                                         # pragma: no cover
          except  TypeMismatch:
                  pass
          
          firstL.extend( secondL, reverse=True )
          assert firstL == [7,9,1,3,5]
          assert isinstance(firstL, EnhList)
          
          print ( "...EnhList.extend tested sucessfully!" )          

                
      #push element to the end
      @logExceptions
      def push(self, *params):
          """
              The methods 'push' and 'pop' implement a FIFO.
              
              'Push' hereby appends to the end of the (enhanced) list.
              
              It accepts no, one or several parameters (elements) to be appended.
              Returns None.
          """
          
          #accept no, one or several parameters
          if    len(params) == 1:
                #one parameter
                retVal = TypedList.append( self, *params )
                
          else:
                #no or several parameters
                retVal = TypedList.extend( self, params )
                
          #print out incoming in debug mode
          if self._debugModeB == True:
             Debug.printt( "--> Element PUSHED into (Enh*)List with id: %d (%s): " % (id(self), self._listNameS), params )
          
          #return None
          return retVal
                
                
      #method testing push
      @classmethod
      def _pushSelftest(cls):
          """ """
          
          print ( "Testing EnhList.push..." )
          
          testL  = EnhList(1,3,5,7)
          test2L = EnhList(1,3,5,7, elemTypesT=(int,float))
          
          #no parameter
          testL.push()
          assert testL == [1,3,5,7]
          test2L.push()
          assert test2L == [1,3,5,7]          
          
          #one parameter
          testL.push(9)
          assert testL == [1,3,5,7,9]
          test2L.push(9)
          try:        
                  test2L.push("a")
                  assert False                                                                                         # pragma: no cover
          except  TypeMismatch:
                  pass          
          assert test2L == [1,3,5,7,9]
          
          #several parameters
          testL.push(11,13,15)
          assert testL == [1,3,5,7,9,11,13,15]
          test2L.push(11,13,15)
          try:        
                  test2L.push(1,"a",2)
                  assert False                                                                                         # pragma: no cover
          except  TypeMismatch:
                  pass          
          assert test2L == [1,3,5,7,9,11,13,15]
          
          print ( "...EnhList.push tested sucessfully!" )                

                                
      #pop element(s) meeting a condition
      @logExceptions
      def pop(self, selector=0, multitude=several):
          """
              The methods 'push' and 'pop' implement a FIFO.
              
              By default (with no parameter given), 'pop' hereby pops from the 
              beginning of the (enhanced) list.
              
              If the parameter 'selector' is a (condition) function resp. partial, taking
              one parameter, namely an element, (just) the elements, for which said
              function resp. partial returns True, are popped.
              
              If, in this situation, the parameter 'multitude' is 'single', just the first
              element meeting said condition is popped (if there is none, None is returned), 
              whereas if it is 'several', all elements meeting said condition are popped.
              
              If on the other hand the 'selector' parameter neither is of type function 
              nor of type partial, it is (just) forwarded to the TypedList.pop method, leading
              to the behaviour of the standard list type resp. 'TypedList'.
          """
             
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be popped
                selectionFunction = selector
          
                if    multitude is single:
                      #just pop the (very) first element meeting the condition
                      for indexI in xrange(TypedList.__len__(self)):
                          if selectionFunction( TypedList.__getitem__(self, indexI) ) == True:
                             retVal = TypedList.pop( self, indexI )
                             
                             #print out outgoing in debug mode
                             if self._debugModeB == True:
                                Debug.printt( "<-- Element POPPED from (Enh*)List with id %d (%s): " % \
                                              (id(self), self._listNameS), retVal                      )
                                
                             return retVal
                          
                      #if no element meets the condition, return None
                      return None
          
                elif  multitude is several:
                      #pop all elements meeting the condition
          
                      popL              = EnhList(elemTypesT=self._elemTypesT)
                      indexI            = TypedList.__len__(self) - 1
                               
                      #process list starting from the end using indices - as the list might be 
                      #modified during processing (by the pops)
                      while indexI >= 0:
                          
                            #just pop elements, for which selectionFunction(element) returns True 
                            if selectionFunction( TypedList.__getitem__(self, indexI) ) == True:
                               popL.insert(0, TypedList.pop( self, indexI ))
                         
                            #next element
                            indexI -= 1
                      
                      #print out outgoing in debug mode
                      if (self._debugModeB == True) and (len(popL) > 0):
                         Debug.printt( "<-- Element POPPED from (Enh*)List with id %d (%s): " % \
                                       (id(self), self._listNameS), popL                        )
                         
                      #return the (enhanced) list containing the popped elements
                      #if no element met the condition, said list is empty
                      return popL                      
                     
                else:
                      raise Exception("The parameter 'multitude' must either be 'single' or 'several'!")
                      
          else:    
                #standard list behaviour 
                #selector should be an index to the element to be popped
                retVal = TypedList.pop(self, selector)
                
                #print out outgoing in debug mode
                if (self._debugModeB == True):
                   Debug.printt( "<-- Element POPPED from (Enh*)List with id %d (%s): " % \
                                 (id(self), self._listNameS), retVal                      )
                   
                return retVal
                
          #unreachable branch
          return None                                                                                                  # pragma: no cover


      #method testing pop
      @classmethod
      def _popSelftest(cls):
          """ """
          
          print ( "Testing EnhList.pop..." )
          
          #no parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop() == 1
          assert testL == [3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #index parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop(4) == 9
          assert testL == [1,3,5,7,11,13,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          poppedL = testL.pop( lambda x: (x > 6) and (x < 10) )
          assert poppedL == [7,9]
          assert isinstance(poppedL, EnhList)
          assert testL == [1,3,5,11,13,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          poppedL = testL.pop( lambda x: (x < 6) or (x > 10) ) 
          assert poppedL == [1,3,5,11,13,15]
          assert isinstance(poppedL, EnhList)
          assert testL == [7,9]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( lambda x: (x > 6), single ) == 7
          assert testL == [1,3,5,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( lambda x: (x > 15), single ) == None
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
                      
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          poppedL = testL.pop( (elem > 6) & (elem < 10) )
          assert poppedL == [7,9]
          assert isinstance(poppedL, EnhList)
          assert testL == [1,3,5,11,13,15]
          assert isinstance(testL, EnhList)
          
          #'partial' function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          poppedL = testL.pop( (elem < 6) | (elem > 10) ) 
          assert poppedL == [1,3,5,11,13,15]
          assert isinstance(poppedL, EnhList)
          assert testL == [7,9]
          assert isinstance(testL, EnhList)
          
          #'partial' function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( (elem > 6), single ) == 7
          assert testL == [1,3,5,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #'partial' function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( (elem > 15), single ) == None
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          print ( "...EnhList.pop tested sucessfully!" )                                          
                
                
      #get element(s) meeting a condition
      @logExceptions
      def __getitem__(self, *params):
          """
              If the first positional parameter between the SQUARE BRACKETS is a (condition) 
              function resp. partial, taking one parameter, namely an element, (just) the 
              elements, for which said function resp. partial returns True, are returned.
              
              If, in this situation, the second parameter is 'single', 
              just the first element meeting said condition is returned 
              (if there is none, None is returned), whereas if it is 'several', 
              all elements meeting said condition are returned. Default is 'several'.
              
              If on the other hand the first positional parameter neither is of type 
              function nor of type partial, the parameters (just) are forwarded to 
              the TypedList.__getitem__ method, leading to the behaviour of the standard 
              list type resp. 'TypedList'.
          """

          #getitem just takes exactly one parameter, this is why, if several
          #are given, e.g. self[a,b], this leads to params == ((a,b),),
          #which is not the common way of passing two parameters to methods
          #the following changes this back to the common way
          paramsT = tuple()
          if (len(params) > 0):
             if     isinstance( params[0], Types_TupleType ):
                    #if params is a tuple containing a tuple (at the first position)
                    paramsT = params[0]
                
             else:
                    #if params is a tuple containing a non-tuple (at the first position)
                    paramsT = params
          
          #one or two 'real' parameters are accepted
          if    len(paramsT) == 1:
                #exactly one positional parameter ==> use it as the selector
                selector  = paramsT[0]
                multitude = several           #use a default for multitude
                
          elif  (len(paramsT) == 2) and (paramsT[1] in (single, several)):
                #two positional parameters and the second either is 'single' or 'several'
                selector  = paramsT[0]
                multitude = paramsT[1]
                
          else:
                raise Exception( "Either one parameter or two parameters - with the "  \
                                 "second being 'single' or 'several' - is allowed!"    )
          
          #check, whether the selector is a function or a 'partial' or something else
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be returned
                selectionFunction = selector
          
                if    multitude is single:
                      #just return the (very) first element meeting the condition
                      for indexI in xrange(TypedList.__len__(self)):
                          if selectionFunction( TypedList.__getitem__(self, indexI) ) == True:
                             return TypedList.__getitem__( self, indexI )
                          
                      #if no element meets the condition, return None
                      return None
          
                elif  multitude is several:
                      #return all elements meeting the condition                
                      return EnhList( [ element for element in self if selectionFunction(element) == True ], \
                                      elemTypesT=self._elemTypesT                                            )
                     
                else:
                      raise Exception("The parameter 'multitude' must either be 'single' or 'several'!")
                      
          else:    
                #forward to standard list behaviour
                retVal = TypedList.__getitem__( self, selector )
                if isinstance(retVal, list):
                   retVal = EnhList(retVal, elemTypesT=self._elemTypesT)
                return retVal
                
          #unreachable branch
          return None                                                                                                  # pragma: no cover
                
                
      #method testing __getitem__
      @classmethod
      def _getitemSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__getitem__..." )
          
          #index parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[4] == 9
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #cross check slicing
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[4:6] 
          assert gotL == [9,11]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #cross check slicing with step with 2
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[2:7:2]
          assert gotL == [5,9,13]
          assert isinstance(gotL, EnhList) 
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[ lambda x: (x > 6) and (x < 10) ] 
          assert gotL == [7,9]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[ lambda x: (x < 6) or (x > 10) ] 
          assert gotL == [1,3,5,11,13,15]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ lambda x: (x > 6), single ] == 7
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ lambda x: (x > 15), single ] == None
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
                      
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[ (elem > 6) & (elem < 10) ]
          assert gotL == [7,9]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #'partial' function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          gotL = testL[ (elem < 6) | (elem > 10) ]
          assert gotL == [1,3,5,11,13,15]
          assert isinstance(gotL, EnhList)
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #'partial' function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ (elem > 6), single ] == 7
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #'partial' function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ (elem > 15), single ] == None
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          print ( "...EnhList.__getitem__ tested sucessfully!" )                 
        
                      
      ##delete element(s) meeting a condition
      @logExceptions
      def __delitem__(self, *params):
          """ 
              If the first positional parameter is a (condition) function resp. partial, 
              taking one parameter, namely an element, (just) the elements, for which said
              function resp. partial returns True, are deleted.
              
              If, in this situation, the second parameter is 'single', 
              just the first element meeting said condition is deleted 
              (if there is none, None is returned), whereas if it is 'several', 
              all elements meeting said condition are deleted. Default is 'several'.
              
              If on the other hand the first positional parameter neither is of type 
              function nor of type partial, the parameter (just) is forwarded to 
              the TypedList.__delitem__ method, leading to the behaviour of the standard 
              list type resp. 'TypedList'.
          """

          #delitem just takes exactly one parameter, this is why, if several
          #are given, e.g. self[a,b], this leads to params == ((a,b),),
          #which is not the common way of passing parameters to methods
          #the following changes this back to the common way
          paramsT = tuple()
          if (len(params) > 0):
             if     isinstance( params[0], Types_TupleType ):
                    #if params is a tuple containing a tuple (at the first position)
                    paramsT = params[0]
                
             else:
                    #if params is a tuple containing a non-tuple (at the first position)
                    paramsT = params
          
          #one or two 'real' parameters are accepted
          if    len(paramsT) == 1:
                #exactly one positional parameter ==> use it as the selector
                selector  = paramsT[0]
                multitude = several
                
          elif  (len(paramsT) == 2) and (paramsT[1] in (single, several)):
                #two positional parameters and the second either is 'single' or 'several'
                selector  = paramsT[0]
                multitude = paramsT[1]
                
          else:
                raise Exception( "Either one parameter or two parameters - with the "  \
                                 "second being 'single' or 'several' - is allowed!"    )
          
          #check, whether the selector is a function or a 'partial' or something else
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be returned
                selectionFunction = selector
          
                if    multitude is single:
                      #just delete the (very) first element meeting the condition
                      for indexI in xrange(TypedList.__len__(self)):
                          if selectionFunction( TypedList.__getitem__(self, indexI) ) == True:
                             return TypedList.__delitem__( self, indexI )
                          
                      #if no element meets the condition, do nothing and return None
                      return None
          
                elif  multitude is several:
                      #delete all elements meeting the condition
          
                      indexI            = TypedList.__len__(self) - 1
                               
                      #process list starting from the end using indices - as the list might be 
                      #modified during processing (by the deletions)
                      while indexI >= 0:
                          
                            #just delete elements, for which selectionFunction(element) returns True 
                            if selectionFunction( TypedList.__getitem__(self, indexI) ) == True:
                               TypedList.__delitem__(self, indexI )
                         
                            #next element
                            indexI -= 1
                          
                      #return the None
                      return None
                     
                else:
                      raise Exception("The parameter 'multitude' must either be 'single' or 'several'!")
                      
          else:    
                #forward to standard list behaviour 
                return TypedList.__delitem__( self, selector )
                
          #unreachable branch
          return None                                                                                                  # pragma: no cover
                
                
      #method testing __getitem__
      @classmethod
      def _delitemSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__delitem__..." )
          
          #index parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[4]
          assert testL == [1,3,5,7,11,13,15]
          assert isinstance(testL, EnhList)
          
          #cross check slicing
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[4:6]
          assert testL == [1,3,5,7,13,15]
          assert isinstance(testL, EnhList)
          
          #cross check slicing with step with 2
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[2:7:2]
          assert testL == [1,3,7,11,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x > 6) and (x < 10) ]
          assert testL == [1,3,5,11,13,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x < 6) or (x > 10) ]
          assert testL == [7,9]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x > 6), single ]
          assert testL == [1,3,5,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x > 15), single ]
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
                      
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem > 6) & (elem < 10) ]
          assert testL == [1,3,5,11,13,15]
          assert isinstance(testL, EnhList)
          
          #'partial' function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem < 6) | (elem > 10) ]
          assert testL == [7,9]
          assert isinstance(testL, EnhList)
          
          #'partial' function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem > 6), single ]
          assert testL == [1,3,5,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          #'partial' function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem > 15), single ]
          assert testL == [1,3,5,7,9,11,13,15]
          assert isinstance(testL, EnhList)
          
          print ( "...EnhList.__delitem__ tested sucessfully!" )
          
          
      #set element(s) meeting a condition
      @logExceptions
      def __setitem__(self, *params):
          """
              If the first positional parameter between the SQUARE BRACKETS is a (condition) 
              function resp. partial, taking one parameter, namely an element, (just) the 
              elements, for which said function resp. partial returns True, are replaced 
              (by the expression to the right of the '=').
              
              If, in this situation, the second parameter is 'single', 
              just the first element meeting said condition is replaced, whereas if it is 
              'several', all elements meeting said condition are replaced. Default is 
              'several'.
              
              If on the other hand the first positional parameter neither is of type 
              function nor of type partial, the parameters (just) are forwarded to 
              the TypedList.__setitem__ method, leading to the behaviour of the standard 
              list type resp. 'TypedList'.
              
              Note that a 'value' is specially treated, if of type 'ConditionFunction'!
          """

          #setitem just takes exactly two parameters, this is why, if more
          #are given, e.g. self[a,b]=c, this leads to params == ((a,b),c),
          #which is not the common way of passing three parameters to methods
          #the following changes this back to the common way: params == (a,b,c).
          paramsT = tuple()
          if (len(params) > 0):
             if     isinstance( params[0], Types_TupleType ):
                    #first parameter is a tuple
                    paramsT = params[0] + (params[1], )
                
             else:
                    #first parameter is NOT a tuple
                    paramsT = params
          
          #two or three 'real' parameters are accepted
          if    len(paramsT) == 2:
                #exactly two positional parameter ==> use the first as the selector
                selector  = paramsT[0]
                multitude = several           #use a default for multitude
                value     = paramsT[1]
                
          elif  (len(paramsT) == 3) and (paramsT[1] in (single, several)):
                #three positional parameters and the second either is 'single' or 'several'
                selector  = paramsT[0]
                multitude = paramsT[1]
                value     = paramsT[2]
                
          else:
                raise Exception( "Either two or three parameters (if three, then the second "  \
                                 "must either be 'single' or 'several') - are allowed!"        )
                                 
          #check parameter 'multitude'
          if multitude not in [single, several]:
             raise Exception("The parameter 'multitude' (second of three) must either be 'single' or 'several'!")
          
          #check, whether the selector is a function or a 'partial' or something else
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be returned
                selectionFunction = selector
          
                for indexI in xrange(TypedList.__len__(self)):
                    currVal = TypedList.__getitem__(self, indexI)
                    
                    #just modify if currVal meets the condition (selector)
                    if selectionFunction( currVal ) == True:
                       if    isinstance(value, ConditionFunction):
                             #'value' is an expression based on the 'element' ConditionFunction - or alike
                             TypedList.__setitem__( self, indexI, value(currVal) )
                             
                       else:
                             TypedList.__setitem__( self, indexI, value )
                       
                       #stop looping if 'single' was chosen
                       if multitude == single:
                          break
                      
          else:    
                #selector is NOT a function - forward it to standard list behaviour
                TypedList.__setitem__( self, selector, value )
                
          #return nothing
          return None
          
          
      #method testing __setitem__
      @classmethod
      def _setitemSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__setitem__..." )
          
          #test standard behaviour
          eL         = EnhList(1,3,5,7,9,11)
          eL[1]      = 4
          assert eL == [1,4,5,7,9,11]
          eL[2:-1]   = [5,-7,-9]
          assert eL == [1,4,5,-7,-9,11]
          eL[::2]    = [0,0,0]
          assert eL == [0,4,0,-7,0,11]
          
          #test additional behaviour
          eL[ elem <= 0 ] = 1
          assert eL == [1,4,1,1,1,11]
          
          eL         = EnhList(1,2,3,4,5,6,7,8,9,10)
          eL[ elem % 2 == 0 ] = elem * 2
          assert eL == [1,4,3,8,5,12,7,16,9,20]
          eL[ (elem == 8) | (elem == 9) ] = (elem + 1) / 2.0
          assert eL == [1,4,3,4.5,5,12,7,16,5.0,20]
          
          #test type checking
          eL         = EnhList(1,2,3,4,5,6,7,8,9,10, elemTypesT=(int,))
          eL[1]      = 22
          eL[ elem == 5 ] = 55
          assert eL == [1,22,3,4,55,6,7,8,9,10]
          
          try:
                 eL[1] = 1.23
                 
          except TypeMismatch:
                 pass
               
          try:
                 eL[ elem == 55 ] = "a"
                 
          except TypeMismatch:
                 pass
               
          assert eL == [1,22,3,4,55,6,7,8,9,10]       
          
          print ( "...EnhList.__setitem__ tested successfully!" )

          
      #check whether element(s) meeting a condition is/are in list
      @logExceptions
      def __contains__(self, selector):
          """
              If the (positional) parameter is a (condition) function resp. partial, 
              taking one parameter, namely an element, __contains__ returns True, if
              the list contains an element, for which said condition function returns 
              True - False otherwise.
              
              If on the other hand the (positional) parameter neither is of type 
              function nor of type partial, the parameter (just) is forwarded to 
              the TypedList.__contains__ method, leading to the behaviour of the standard 
              list type resp. 'TypedList'.
          """
          
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for elements checked for
                selectionFunction = selector
          
                #just search until one element meeting the condition has been found
                for indexI in xrange(TypedList.__len__(self)):
                    if selectionFunction( TypedList.__getitem__(self, indexI) ) == True:
                       #one element meeting the condition found
                       return True
                          
                #if no element met the condition, return False
                return False
          
          else:    
                #standard list behaviour 
                #selector should be an index to the element to be deleted
                return TypedList.__contains__(self, selector) 
                
          #unreachable branch
          return None                                                                                                  # pragma: no cover
                
                
      #method testing __contains__
      @classmethod
      def _containsSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__contains__..." )
          
          #object
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert 7 in testL
              
          #(lambda) function parameter - logical 'and'
          assert (lambda x: (x > 5) and (x < 9)) in testL
          
          #(lambda) function parameter - logical 'or'
          assert (lambda x: (x < 1) or (x > 15)) not in testL
          
          #'partial' parameter - logical 'or' and 'and'
          assert (((elem == 3) | (elem == 7)) & ((elem > 4) | (elem < 4))) in testL
          assert isinstance(testL, EnhList)
          
          print ( "...EnhList.__contains__ tested sucessfully!" )                 
        
   
      #check whether all elements of the list meet an condition
      @logExceptions
      def areAll(self, conditionFct):
          """ 
              Checks whether all elements of the list meet the condition
              described by the parameter conditionFct - which either can be a
              function or a 'partial' (inheritors are fine too).
              
              If conditionFct is True for all elements, True is returned - 
              False otherwise.
          """
          
          #ensure, that conditionFct is a function or a 'partial'
          assert isinstance(conditionFct, (Types_FunctionType, Functools_partial)),                           \
                 "The parameter 'conditionFct' must either be of type function or of type 'partial'!"
                 
          #just search until one element does not meet the condition has been found
          for indexI in xrange(TypedList.__len__(self)):
              if conditionFct( TypedList.__getitem__(self, indexI) ) == False:
                 #(at least) one element does not meet the condition
                 return False
                    
          #all elements met the condition
          return True
          
                                        
      #method testing areAll
      @classmethod
      def _areAllSelftest(cls):
          """ """
          
          print ( "Testing EnhList.areAll..." )
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.areAll( lambda x: (x >= 1) and (x <= 15) )
          
          #(lambda) function parameter - logical 'or'
          assert testL.areAll( lambda x: (x >= 9) or (x <= 10) )
          
          #'partial' parameter - logical 'and'
          assert testL.areAll( (elem >= 1) & (elem <= 15) )
          
          #'partial' parameter - logical 'or'
          assert testL.areAll( (elem >= 9) | (elem <= 10) )

          #'partial' parameter - logical 'or'
          assert not testL.areAll( (elem >= 11) | (elem <= 8) )
          assert isinstance(testL, EnhList)
          
          print ( "...EnhList.areAll tested sucessfully!" ) 


      #map function to all elements meeting condition
      @logExceptions
      def mapIf(self, *params):
          """ 
               The first positional parameter 'mapO' is the 
               function / 'partial' / object to be  
               mapped to the list elements (inheritors are fine too). 
               
               The second positional parameter 'conditionFct' is the 
               condition function / 'partial'
               - the mapping just is done for list elements, which meet said 
               condition (means: for which the condition function returns True).
               
               If the (second positional) parameter 'conditionFct' is omitted, 
               it defaults to: 'lambda x: True' (means: True in any case).
               
               Mapping means: replacing each element (meeting 'conditionFct') 
               by 'mapO(element)'.
          """
             
          #method accepts one or two parameters          
          if    len(params) == 1:
                #map all elements
                mapO = params[0]
                
                #ensure the correct type for mapO
                assert isinstance(mapO, (Types_FunctionType, Functools_partial, object)), \
                       "First positional parameter 'mapO' has the wrong type!"
                
                #map mapO to all elements - in-place
                for indexI in xrange(TypedList.__len__(self)):
                   TypedList.__setitem__( self, indexI, mapO(TypedList.__getitem__(self, indexI)) )
                 
          elif  len(params) == 2:
                #just map elements, meeting the condition
                mapO         = params[0]
                conditionFct = params[1] 
                
                #ensure the correct type for mapO and conditionFct
                assert isinstance(mapO,         (Types_FunctionType, Functools_partial, object))          and \
                       isinstance(conditionFct, (Types_FunctionType, Functools_partial, Types_NoneType)),     \
                       "Parameter types do not fit!"                
                
                #map mapO to all elements, for which conditionFct returns True - in place
                for indexI in xrange(TypedList.__len__(self)):
                    if conditionFct( TypedList.__getitem__(self, indexI) ) == True:
                       TypedList.__setitem__( self, indexI, mapO(TypedList.__getitem__(self, indexI)) )
                       
          else:
                raise Exception("Method expects one or two parameters!")
                
          #just to be clear
          return None
          
          
      #method testing map-if
      @classmethod
      def _mapIfSelftest(cls):
          """ """
          
          print ( "Testing EnhList.mapIf..." )
          
          #(lambda) function parameter
          testL = EnhList(1,3,5,7,9)
          testL.mapIf( lambda x: x*2 )
          assert testL == [2,6,10,14,18]
          assert isinstance(testL, EnhList)
          
          #object parameter
          testL = EnhList(1,3,5,7,9)
          class testO(object):
                def __init__(self, value):
                    self.abc = value
          testL.mapIf( testO )
          assert [element.abc for element in testL] == [1,3,5,7,9]
          assert isinstance(testL, EnhList)
          
          ### with condition ###
          #(lambda) function parameter
          testL = EnhList(range(1,10))
          testL.mapIf( lambda x: x*2, lambda x: x % 2 == 0)
          assert testL == [1,4,3,8,5,12,7,16,9]
          assert isinstance(testL, EnhList)
          
          #object parameter
          testL = EnhList(range(1,10))
          class testO(object):
                def __init__(self, value):
                    self.abc = value
                def __repr__(self):
                    return "abc=%s" % self.abc
                def __eq__(self, ohs):
                    return (True if self.abc == ohs else False)
          testL.mapIf( testO, elem > 5 )
          assert testL == [1,2,3,4,5,testO(6),testO(7),testO(8),testO(9)]
          assert isinstance(testL, EnhList)
          
          #partial function parameter
          testL = EnhList(1,3,5,7,9)
          testL.mapIf( elem * 2, elem > 5 )
          assert testL == [1,3,5,14,18]
          assert isinstance(testL, EnhList)
          
          #in typed mode
          testL = EnhList(1,3,5,7,9, elemTypesT=(int, float))
          testL.mapIf( lambda x: x*2, elem < 5 )
          assert testL == [2,6,5,7,9]
          assert isinstance(testL, EnhList)
          
          testL = EnhList(1,3,5,7,9, elemTypesT=(int, float))
          try:
                 testL.mapIf( lambda x: "a" * x, elem < 5 )
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          assert testL == [1,3,5,7,9]
          assert isinstance(testL, EnhList)

          print ( "...EnhList.mapIf tested sucessfully!" )           
          
          
      #applymap function to all elements meeting condition
      @logExceptions
      def applyMapIf(self, *params):
          """ 
               The first positional parameter 'mapO' is the 
               function / 'partial' / object to be  
               apply-mapped to the list elements (inheritors are fine too). 
               
               The second positional parameter 'conditionFct' is the 
               condition function / 'partial'
               - the mapping just is done for list elements, which meet said 
               condition (means: for which the condition function returns True).
               
               If the (second positional) parameter 'conditionFct' is omitted, 
               it defaults to: 'lambda x: True' (means: True in any case).
               
               Apply-mapping means: applying 'mapO' to each element 
               (meeting 'conditionFct'). Said elements are not replaced as they
               would be when using 'self.mapIf' instead.
          """
             
          #method accepts one or two parameters          
          if    len(params) == 1:
                #map all elements
                mapO = params[0]
                
                #ensure the correct type for mapO
                assert isinstance(mapO, (Types_FunctionType, Functools_partial, object)), \
                       "First positional parameter 'mapO' has the wrong type!"
                
                #map mapO to all elements - in-place                
                if    not isinstance(self._elemTypesT, tuple):
                      #without type checking
                      for indexI in xrange(TypedList.__len__(self)):
                          mapO(TypedList.__getitem__(self, indexI))
                          
                else:
                      #with type checking
                      for indexI in xrange(TypedList.__len__(self)):
                          mapped = mapO(TypedList.__getitem__(self, indexI))
                          
                          #check type
                          if isinstance(mapped, self._elemTypesT):
                             raise TypeMismatch( "Elements resulting from applyMap must all be of any type of "     \
                                                 "%s (not '%s' of '%s')" % (self._elemTypesT, mapped, type(mapped)) )
                 
          elif  len(params) == 2:
                #just map elements, meeting the condition
                mapO         = params[0]
                conditionFct = params[1] 
                
                #ensure the correct type for mapO and conditionFct
                assert isinstance(mapO,         (Types_FunctionType, Functools_partial, object))          and \
                       isinstance(conditionFct, (Types_FunctionType, Functools_partial, Types_NoneType)),     \
                       "Parameter types do not fit!"                
                
                #map mapO to all elements, for which conditionFct returns True - in place
                if    not isinstance(self._elemTypesT, tuple):
                      #without type checking
                      for indexI in xrange(TypedList.__len__(self)):
                          if conditionFct( TypedList.__getitem__(self, indexI) ) == True:
                             mapO(TypedList.__getitem__(self, indexI))
                             
                else:
                      #with type checking
                      for indexI in xrange(TypedList.__len__(self)):
                          if conditionFct( TypedList.__getitem__(self, indexI) ) == True:
                             mapped = mapO(TypedList.__getitem__(self, indexI))
                             
                             #check type
                             if isinstance(mapped, self._elemTypesT):
                                raise TypeMismatch( "Elements resulting from applyMap must all be of any type of "     \
                                                    "%s (not '%s' of '%s')" % (self._elemTypesT, mapped, type(mapped)) )
                       
          else:
                raise Exception("Method expects one or two parameters!")
                
          #just to be clear
          return None
              
              
      #method testing apply-map
      @classmethod
      def _applyMapIfSelftest(cls):
          """ """
          
          print ( "Testing EnhList.applyMapIf..." )
          
          #(lambda) function parameter
          testL = EnhList(( [index, index] for index in range(3) ))
          testL.applyMapIf( lambda x: list.__setitem__(x, 1, 111) )
          testL.applyMapIf( lambda x: x.append(222) )
          assert testL == [[0, 111, 222], [1, 111, 222], [2, 111, 222]]
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - in type check mode
          testL = EnhList(( [index, index] for index in range(3) ), elemTypesT=(tuple,list))
          testL.applyMapIf( lambda x: list.__setitem__(x, 1, 111) )
          testL.applyMapIf( lambda x: x.append(222) )
          assert testL == [[0, 111, 222], [1, 111, 222], [2, 111, 222]]
          assert isinstance(testL, EnhList)
                             
          ### with condition ###
          #(lambda) function parameter
          testL = EnhList(( [index, index] for index in range(5) ))
          testL.applyMapIf( lambda x: list.__setitem__(x, 1, 111), lambda x: x[0] % 2 == 0 )
          testL.applyMapIf( lambda x: x.append(222), lambda x: x[0] % 2 == 1 )
          assert testL == [[0, 111], [1, 1, 222], [2, 111], [3, 3, 222], [4, 111]] 
          assert isinstance(testL, EnhList)
          
          #(lambda) function parameter - in type check mode
          testL = EnhList(( [index, index] for index in range(5) ), elemTypesT=(tuple,list))
          testL.applyMapIf( lambda x: list.__setitem__(x, 1, 111), lambda x: x[0] % 2 == 0 )
          testL.applyMapIf( lambda x: x.append(222), lambda x: x[0] % 2 == 1 )
          assert testL == [[0, 111], [1, 1, 222], [2, 111], [3, 3, 222], [4, 111]] 
          assert isinstance(testL, EnhList)          

          print ( "...EnhList.applyMapIf tested sucessfully!" )    


      #create wrapper methods, which ensure, that all lists returned are of type EnhList
      if    isPy2() == True:
            methodNamesT = ( "__getslice__", "__add__", "__mul__", "__rmul__" )
          
      else:
            methodNamesT = ( "__add__", "__mul__", "__rmul__" )
          
      for methodNameS in methodNamesT:
          #create methods using exec
          exec("""@logExceptions
def {0}(self, *params, **paramDict):
    ' A wrapper, which ensure that lists returned are of type EnhList. '
    
    #keep standard behaviour of standard list resp. TypedList
    retVal = TypedList.{0}(self, *params, **paramDict)
    
    #ensure that return value is an EnhList - with the same type list, if any
    if isinstance(retVal, list):
       retVal = EnhList( retVal, elemTypesT=self._elemTypesT )
       
    #return value
    return retVal
               """.format(methodNameS))
             
      del methodNamesT
      del methodNameS
               
               
      #method testing mapAll
      @classmethod
      def _addSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__add__..." )
          
          ### __add__ ###
          #no type checking
          testL = EnhList(1,3,5)
          testL = testL + [7,9]
          assert testL == [1,3,5,7,9]
          assert isinstance(testL, EnhList)
          assert testL._elemTypesT == None
          
          #type checking mode
          testL = EnhList(1,3,5, elemTypesT=(int,float))
          testL = testL + [7,9]
          assert testL == [1,3,5,7,9]
          assert isinstance(testL, EnhList)
          assert testL._elemTypesT == (int,float)
          
          #no type checking
          testL = EnhList(1,3,5)
          testL = testL + [7,"a"]
          assert testL == [1,3,5,7,"a"]
          assert isinstance(testL, EnhList)
          assert testL._elemTypesT == None
          
          #type checking mode
          testL = EnhList(1,3,5, elemTypesT=(int,float))
          try:
                 testL = testL + [7,"a"]
                 assert False                                                                                         # pragma: no cover
          except TypeMismatch:
                 pass
          assert testL == [1,3,5]
          assert isinstance(testL, EnhList)
          assert testL._elemTypesT == (int,float)
          
          ### __iadd__ ###
          #no type checking
          testL  = EnhList(1,3,5)
          testL += [7,9]
          assert testL == [1,3,5,7,9]
          assert isinstance(testL, EnhList)
          assert testL._elemTypesT == None
          
          #type checking mode
          testL  = EnhList(1,3,5, elemTypesT=(int,float))
          testL += [7,9]
          assert testL == [1,3,5,7,9]
          assert isinstance(testL, EnhList)
          assert testL._elemTypesT == (int,float)
          
          #no type checking
          testL  = EnhList(1,3,5)
          testL += [7,"a"]
          assert testL == [1,3,5,7,"a"]
          assert isinstance(testL, EnhList)
          assert testL._elemTypesT == None
          
          #type checking mode
          testL = EnhList(1,3,5, elemTypesT=(int,float))
          try:
                 testL += [7,"a"]
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          assert testL == [1,3,5]
          assert isinstance(testL, EnhList)
          assert testL._elemTypesT == (int,float)
          
          print ( "...EnhList.__add__ tested sucessfully!" )
               
               
      #get min
      @logExceptions
      def min(self, propertySelFct=elem):
          """
               Maps the property selector (partial) function 'propertySelFct'
               to self resp. to all elements of self and, after that, returns
               the minimum of the resulting values.
          """
          
          if    isPy2() == True:
                cloneL = list.__getslice__(self, 0, list.__len__(self))
              
          else:
                cloneL = list.__getitem__(self, slice(0, list.__len__(self), None))
          
          return min( map( propertySelFct, cloneL ) )
          
          
      #get max
      @logExceptions
      def max(self, propertySelFct=elem):
          """
               Maps the property selector (partial) function 'propertySelFct'
               to self resp. to all elements of self and, after that, returns
               the maximum of the resulting values.       
          """
          
          if    isPy2() == True:
                cloneL = list.__getslice__(self, 0, list.__len__(self))
              
          else:
                cloneL = list.__getitem__(self, slice(0, list.__len__(self), None))
          
          return max( map( propertySelFct, cloneL ) )
          
          
      #get sum
      @logExceptions
      def sum(self, propertySelFct=elem):
          """
               Maps the property selector (partial) function 'propertySelFct'
               to self resp. to all elements of self and, after that, returns
               the sum of the resulting values.          
          """
          
          if    isPy2() == True:
                cloneL = list.__getslice__(self, 0, list.__len__(self))
              
          else:
                cloneL = list.__getitem__(self, slice(0, list.__len__(self), None))
          
          return sum( map( propertySelFct, cloneL ) )          
          
          
      #get average
      @logExceptions
      def avg(self, propertySelFct=elem):
          """
               Maps the property selector (partial) function 'propertySelFct'
               to self resp. to all elements of self and, after that, returns
               the average of the resulting values.          
          """
          
          if    isPy2() == True:
                cloneL = list.__getslice__(self, 0, list.__len__(self))
              
          else:
                cloneL = list.__getitem__(self, slice(0, list.__len__(self), None))
          
          summ = sum( map( propertySelFct, cloneL ) )
          
          return float( summ ) / float( list.__len__(self) )
          
          
      #get median
      @logExceptions
      def median(self, propertySelFct=elem):
          """
               Maps the property selector (partial) function 'propertySelFct'
               to self resp. to all elements of self and, after that, returns
               the median of the resulting values.          
          """
          
          if    list.__len__(self)     <= 0:
                #no element
                raise FatalError("The median of an empty list is undefined!")
                
          elif  list.__len__(self)     == 1:
                #a single element
                return float( propertySelFct( list.__getitem__(self, 0) ) )
                
          elif  list.__len__(self) % 2 == 0:
                #even number of elements
                if    isPy2() == True:
                      cloneL = list.__getslice__(self, 0, list.__len__(self))
                    
                else:
                      cloneL = list.__getitem__(self, slice(0, list.__len__(self), None))                      
                
                sortedL = sorted( map(propertySelFct, cloneL) )
                midstI  = list.__len__(self) // 2
                return float(sortedL[midstI-1] + sortedL[midstI]) / 2.0
                
          else:
                #odd number of elements          
                if    isPy2() == True:
                      cloneL = list.__getslice__(self, 0, list.__len__(self))
                    
                else:
                      cloneL = list.__getitem__(self, slice(0, list.__len__(self), None))
                      
                sortedL = sorted( map(propertySelFct, cloneL) )
                midstI  = list.__len__(self) // 2
                return float(sortedL[midstI])
                
          #unreachable branch
          return None                                                                                                  # pragma: no cover
                
                
      #method testing min, max, avg and median
      @classmethod
      @muteLogging
      def _minMaxAvgMedianSelftest(cls):
          """ """
          
          print ( "Testing EnhList.min, .max, .sum, .avg and .median..." )
          
          enhList = EnhList( [3] )
          assert enhList.min() == enhList.max() == enhList.avg() == enhList.median() == 3
          
          enhList = EnhList( [3,4] )
          assert enhList.min() == 3
          assert enhList.max() == 4
          assert enhList.avg() == enhList.median() == 3.5
          assert enhList.sum() == 7
          
          enhList = EnhList( [3,5,7] )
          assert enhList.min() == 3
          assert enhList.max() == 7
          assert enhList.avg() == enhList.median() == 5
          assert enhList.sum() == 15
          
          enhList = EnhList( [3,5,7,9] )
          assert enhList.min() == 3
          assert enhList.max() == 9
          assert enhList.avg() == enhList.median() == 6
          
          enhList = EnhList( [3,5,7,9,11] )
          assert enhList.min() == 3
          assert enhList.max() == 11
          assert enhList.avg() == enhList.median() == 7
          
          enhList = EnhList( [7,7,7,11,11] )
          assert enhList.min()    == 7
          assert enhList.max()    == 11
          assert enhList.avg()    == 8.6
          assert enhList.median() == 7
          
          elemsL  = [(1,2),(3,4),(5,6),(7,8),(9,10)]
          elemsL  = [dict(a=element[0], b=element[1]) for element in elemsL]
          enhList = EnhList( elemsL )
          assert enhList.min( elem["a"] ) == 1
          assert enhList.min( elem["b"] ) == 2
          assert enhList.max( elem["a"] ) == 9
          assert enhList.max( elem["b"] ) == 10
          assert enhList.avg( elem["a"] ) == 5
          assert enhList.avg( elem["b"] ) == 6
          assert enhList.sum( elem["a"] ) == 25
          assert enhList.sum( elem["b"] ) == 30          
          assert enhList.median( elem["a"] ) == 5
          assert enhList.median( elem["b"] ) == 6
          
          print ( "...EnhList.min, .max, .sum, .avg and .median tested sucessfully!" )                
               

      #method testing self
      @classmethod
      def _selftest(cls):            
          """
              If no exception is raised during the execution of this method 
              the EnhList class behaves as expected.
              
              It e.g. can be used to check the integrity after modifications
              or to check the compatibility with specific python versions.
              
              Have a look into the methods called in this method for examples,
              how EnhList can be used.
          """
          
          print ( "Testing EnhList..." )
          
          cls._initSelftest()
          cls._pushSelftest()
          cls._popSelftest()
          cls._extendSelftest()
          cls._getitemSelftest()
          cls._delitemSelftest()
          cls._setitemSelftest()
          cls._containsSelftest()
          cls._areAllSelftest()
          cls._mapIfSelftest()
          cls._applyMapIfSelftest()
          cls._addSelftest()
          cls._minMaxAvgMedianSelftest()
          
          #test, whether all returned lists are EnhList-s
          eL = EnhList(1,3,5,7,9,11,13)
          assert isinstance( eL,               EnhList )
          assert isinstance( eL[2:4],          EnhList )
          assert isinstance( eL[2::2],         EnhList )
          assert isinstance( eL + [15,17],     EnhList )
          assert isinstance( eL * 3,           EnhList )
          assert isinstance( 3 * eL,           EnhList )
          assert isinstance( eL[elem > 3],     EnhList )
          assert isinstance( eL.pop(elem > 3), EnhList )
          
          #in type checking mode
          eL = EnhList(1,3,5,7,9,11,13, elemTypesT=(int,float))
          assert isinstance( eL,               EnhList )
          assert eL._elemTypesT == (int,float)
          assert isinstance( eL[2:4],          EnhList )
          assert eL[2:4]._elemTypesT == (int,float)
          assert isinstance( eL[2::2],         EnhList )
          assert eL[2::2]._elemTypesT == (int,float)
          assert isinstance( eL + [15,17],     EnhList )
          assert (eL + [15,17])._elemTypesT == (int,float)
          assert isinstance( eL * 3,           EnhList )
          assert (eL * 3)._elemTypesT == (int,float)
          assert isinstance( 3 * eL,           EnhList )
          assert (3 * eL)._elemTypesT == (int,float)
          assert isinstance( eL[elem > 3],     EnhList )
          assert eL[elem > 3]._elemTypesT == (int,float)
          assert isinstance( eL.pop(elem > 3), EnhList )
          assert eL.pop(elem > 3)._elemTypesT == (int,float)
          
          print ( "...EnhList tested sucessfully!" )
          

          
class SemiBlockingMutex(object):
      """ 
          Locks normally either are blocking or non-blocking.
          
          Whereas this mutex is a lock, which is neither nor - it (just) is temporarily
          blocking. It blocks (just) until the internal lock either has been acquired 
          successfully or until a maximal total timeout (parameter 'timeoutMsF') 
          has expired.
          
          Until that, the 'acquire' method of the internal lock is polled. The time 
          interval/duration between two such polls is random - but it is in the range 
          given by the polling interval range tuple (parameter 'pollIntervalRangeMsT').
          
          Note, that the minimum of said range always is taken as the very first
          polling resp. sleep interval/duration. Just the following polling resp.
          sleep intervals/durations are random then - if any further (necessary at all).
          
          This mutex comes with the known 'acquire' and 'release' methods as well as 
          with context manager methods.

          Example:
          mutex = SemiBlockingMutex('mt_semi_blocking')     #alternative: 'mp_semi_blocking'
          with mutex: 
               print 'Mutex locked before this and unlocked after this - both automatically.' 
      """
      
      _lock                 = None      #either a threading.Lock or a multiprocessing.Lock
      _timeoutBucketMsF     = None      #contains the time left for acquiring successfully
      
      _timeoutMsF           = None      #max total timeout in ms - initial time bucket value
      _pollIntervalRangeMsT = None      #(min,max) single timeout time in ms
      
      _enterCntI             = None     #just used for the selfttests
      _exitCntI              = None     #just used for the selfttests


      #constructor
      @logExceptions
      def __init__( self, lockTypeS="mp_semi_blocking",                  \
                    timeoutMsF=5000.0, pollIntervalRangeMsT=(0.05, 5.0) ):
          """ 
               The keyword parameter 'lockTypeS' either must be 'mt_semi_blocking' or 'mp_semi_blocking'
               - first leads to using a threading.Lock internally, second to multiprocessing.Lock.
               
               The 'acquire' method just blocks temporarily, the belonging total timeout is given               
               by the parameter 'timeoutMsF'.
               
               The parameter 'pollIntervalRangeMsT' determines the mean polling frequency during
               said temporary blocking phases.                              
          """
                    
          #init lock - either threading.Lock or multiprocessing.Lock
          if    lockTypeS  == "mt_semi_blocking":
                self._lock  = Threading_Lock()
                
          elif  lockTypeS  == "mp_semi_blocking":
                self._lock  = Multiprocessing_Lock()
                
          else:
                raise Exception("The keyword parameter 'lockTypeS' either must be 'mt_semi_blocking' or 'mp_semi_blocking'!")
                
          #init total timeout and polling interval
          self._timeoutMsF           = timeoutMsF
          self._pollIntervalRangeMsT = pollIntervalRangeMsT
          
          #init variables for selftest
          self._enterCntI = 0
          self._exitCntI  = 0


      #blocks until SemiBlockingMutex is unlocked or a timeout has expired
      @logExceptions
      def acquire(self):
          """ 
              Polls 'acquire' until the internal lock has been acquired successfully - or
              until the self._timeoutBucketMsF has become empty.
              
              If SemiBlockingMutex is resp. becomes unlocked in time, the return value 
              is True (False otherwise). 
          """
          
          #reset timeout bucket
          self._timeoutBucketMsF = self._timeoutMsF
          
          #first poll 
          if self._lock.acquire(False) == True:
             return True
          
          #sleep minimal time
          minTimeMsF = min(self._pollIntervalRangeMsT)
          Time_sleep( minTimeMsF / 1000.0 )
          self._timeoutBucketMsF -= minTimeMsF
          
          #prepare random 'iterator' for the loop
          maxTimeMsF = max(self._pollIntervalRangeMsT)
          nextPollIntervalMsFct = Functools_partial( Random_uniform, minTimeMsF, maxTimeMsF )
          
          #retry acquiring until successful or timeout expired
          while self._lock.acquire(False) == False:
                
                #block this thread temporarily
                currTimeMsF = nextPollIntervalMsFct()
                Time_sleep( currTimeMsF / 1000.0 )
                
                #check for timeout
                self._timeoutBucketMsF -= currTimeMsF
                if self._timeoutBucketMsF <= 0:
                   #acquiring failed
                   return False

          #acquiring successful
          return True
          
          
      @logExceptions
      def release(self):
          """ Releases the lock. Just a forward to self._lock.release(). """

          return self._lock.release()           


      #enter context
      @logExceptions
      def __enter__(self):
          """ Context is just entered if SemiBlockingMutex is resp. has successfully been unlocked.
              An exception is raised otherwise. """

          #increment counter for selftests
          self._enterCntI += 1    
          
          #acquire lock
          if self.acquire() == False:
             raise Exception('SemiBlockingMutex blocked too long (and is still locked)!')
             
          #return mutex itself for 'as' - if any
          return self


      #exit context
      @logExceptions
      def __exit__(self, *exception):
          """ When context is left, unlock SemiBlockingMutex in any case (as it has been acquired by
              entering said context before). """

          #increment counter for selftests
          self._exitCntI += 1
          
          #release lock
          self._lock.release() 
          
          #return None
          return None
          
          
          
class BlockingMutex(object):
      """           
          This mutex comes with the known 'acquire' and 'release' methods as well as 
          with context manager methods.

          Example:
          mutex = BlockingMutex('mt_blocking')     #alternative: 'mp_blocking'
          with mutex: 
               print 'Mutex locked before this and unlocked after this - both automatically.' 
      """
      
      _lock                 = None      #either a threading.Lock or a multiprocessing.Lock
      
      _enterCntI             = None     #just used for the selfttests
      _exitCntI              = None     #just used for the selfttests


      #constructor
      @logExceptions
      def __init__( self, lockTypeS="mt_blocking" ):
          """ 
               The keyword parameter 'lockTypeS' either must be 'mt_blocking' or 'mp_blocking'
               - first leads to using a threading.Lock internally, second to multiprocessing.Lock.                             
          """
                    
          #init lock - either threading.Lock or multiprocessing.Lock
          if    lockTypeS  == "mt_blocking":
                self._lock  = Threading_Lock()
                
          elif  lockTypeS  == "mp_blocking":
                self._lock  = Multiprocessing_Lock()
                
          else:
                raise Exception("The keyword parameter 'lockTypeS' either must be 'mt_blocking' or 'mp_blocking'!")
          
          #init variables for selftest
          self._enterCntI = 0
          self._exitCntI  = 0


      #blocks until BlockingMutex is unlocked
      @logExceptions
      def acquire(self):
          """ Acquire the lock. Just a forward to self._lock.acquire(True). """
          
          return self._lock.acquire(True)
                
          
      @logExceptions
      def release(self):
          """ Releases the lock. Just a forward to self._lock.release(). """

          return self._lock.release()           


      #enter context
      @logExceptions
      def __enter__(self):
          """ Context is entered as soon as if BlockingMutex is resp. has 
              successfully been unlocked.
          """

          #increment counter for selftests
          self._enterCntI += 1    
          
          #acquire lock
          self.acquire()
             
          #return mutex itself for 'as' - if any
          return self


      #exit context
      @logExceptions
      def __exit__(self, *exception):
          """ When context is left, unlock BlockingMutex in any case (as it has been acquired by
              entering said context before). """

          #increment counter for selftests
          self._exitCntI += 1
          
          #release lock
          self.release() 
          
          #return None
          return None
              


#######################
# Secured List Class  #
#######################
class SecList(EnhList):
      """ 
          A 'SecList' is a wrapped 'EnhList' whereby the wrapper ensures,
          that access to the content of the list via an intrinsic access 
          method listed in 'self.lockedMethodsT' automatically is secured 
          by an internal threading or multiprocessing lock ('self._lock') 
          - in particular in-place operations are affected; this is 
          achieved by wrapping said access methods in a 'with' context. 
          
          If, on the other hand, such a locked access method is called 
          inside of a manually entered 'with' context (using the 
          built-in 'with' command) of 'SecList', access alredy is
          (manually) secured and the 'with' of said wrapper is NOT
          called - to prevent accidental dead locks.
          
          When such a 'with' context is entered, the 'self.__enter__' 
          method is called - which 'acquire's said lock. When said 
          'with' context after that is left, the 'self.__exit__' method
          is called - which 'release's said lock.
          
          Said lock is a 'BlockingMutex("mp_blocking")' per default, but 
          another one, e.g. a 'SemiBlockingMutex()', which blocks, but 
          just temporarily (due to a timeout), can also be chosen. Also 
          have a look at the doc string texts of 'BlockingMutex' and 
          'SemiBlockingMutex' for further informations.
          
          Simple example for an automatically secured (thread-safe) access:
          -----------------------------------------------------------------
          
          sL = SecList(1,3,5,7)                   #sL: [1,3,5,7]
          nL = sL[ (elem > 1) & (elem < 7) ]      #nL: [3,5]
          
          A more extensive example for safe multi threaded access can be 
          found in 'SecList._selftest'.

          The iterator protocol is not (automatically) wrapped / secured
          - (it does not call an intrinsic method listed in 
          'self.lockedMethodsT'); if thread safety is not necessary, but 
          performance is, then iterator access can be used on 'SecList'-s. 
          But you of course also can secure it manually by using the 'with' 
          statement.
          
          Simple example for a manually secured (thread-safe) access:
          -----------------------------------------------------------
          
          sL = SecList(1,3,5,7)                    #sL: [1,3,5,7]
          with sL:           
               nL = [element+1 for element in sL]  #nL: [2,4,6,8]
               
          Further examples can be found in 'SecList._selftest'.
          
          Extrinsic functions alike the built-ins 'all', 'any', 'apply',
          'filter', 'map', 'reduce', 'sorted' and 'reversed' or the 
          'pickle.dumps/loads' aren't automatically secured too (they 
          do not call an intrinsic method listed in 'self.lockedMethodsT' 
          too). They can be manually secured in the same way as described
          above for the iterator protocol / example.
          
          But note, that extrinsic functions might not return a 'SecList' 
          but e.g. a 'list' instead or even might not work on a 'SecList' 
          at all (e.g. pickle - pickling locks is not possible).
            
          The same care should be taken for in-place arithmetic operators
          and '__radd__' related stuff alike:
          
          sL[1] += 1       #not thread safe (getting and setting is 
                           #automatically locked, but not the time 
                           #between them)
          3 + sL           #not implemented
          
          You might want to use a manual 'with' context around such
          actions or you might want to convert the 'SecList' to a 
          'list' by slicing it before you use said functions on it, 
          or... For example:
          
          with sL:         #manually locked 
               sL[1] += 1
          3 + sL[:]        #slicing is automatically locked
          
     
          
          Parameters: 
          -----------
              
          Just positional parameters and the following keyword parameters
          are valid: 
          
          'elemTypesT', 'lockTypeS', 'timeoutMsF' and 'pollIntervalRangeMsT'.
          
          Positional parameters are forwarded to the constructor of the
          parent class 'EnhList'; have a look at the doc string of 'EnhList'
          for details concerning the meaning / usage of positional parameters.
          
          The keyword parameter 'elemTypesT' is forwarded to the constructor
          of the parent class 'EnhList' too - which then again forwards it to
          the constructor of its own parent class 'TypedList'; have a look at
          the doc string of 'TypedList' for details concerning the meaning /
          usage of 'elemTypesT'.
          
          The keyword parameter 'lockTypeS' determines, which kind of lock is
          used to secure access to the elements of the list. Possible options
          are:
          
          "mt_blocking"      ==> BlockingMutex(     "mt_blocking"     ) is used.
          "mp_blocking"      ==> BlockingMutex(     "mp_blocking"     ) is used.
          "mt_semi_blocking" ==> SemiBlockingMutex( "mt_semi_blocking") is used.
          "mp_semi_blocking" ==> SemiBlockingMutex( "mp_semi_blocking") is used.
          
          Have a look at the doc string of 'BlockingMutex' resp. 
          'SemiBlockingMutex' for details concerning the meaning of said options.
          If no keyword parameter '' is given, the default 
          'BlockingMutex("mp_blocking")' is used.
          
          The keyword parameters 'timeoutMsF' and 'pollIntervalRangeMsT' are
          forwarded to the constructor of said 'SemiBlockingMutex' - if chosen;
          they are not valid for 'BlockingMutex' lock types.
      """
      
      _lock           = None       #the lock used
      _inWithContextB = None       #whether list yet is in 'with' context ('self.__enter__' has been called) or not
      
      if    isPy2() == True:
            lockedMethodsT = ( "__add__", "__contains__", "__delitem__", "__delslice__", "__eq__",  \
                               "__ge__", "__getitem__", "__getslice__", "__gt__",                   \
                               "__iadd__", "__imul__", "__le__", "__len__", "__lt__", "__mul__",    \
                               "__ne__", "__repr__", "__reversed__",                                \
                               "__rmul__", "__setitem__", "__setslice__", "__sizeof__",             \
                               "append", "areAll", "count", "extend", "index", "insert", "mapIf",   \
                               "pop", "push", "remove", "reverse", "sort", "applyMapIf", "min",     \
                               "max", "sum", "avg", "median"                                        )
      else:
            lockedMethodsT = ( "__add__", "__contains__", "__delitem__", "__eq__",                  \
                               "__ge__", "__getitem__", "__gt__",                                   \
                               "__iadd__", "__imul__", "__le__", "__len__", "__lt__", "__mul__",    \
                               "__ne__", "__repr__", "__reversed__",                                \
                               "__rmul__", "__setitem__", "__sizeof__",                             \
                               "append", "areAll", "count", "extend", "index", "insert", "mapIf",   \
                               "pop", "push", "remove", "reverse", "sort", "applyMapIf", "min",     \
                               "max", "sum", "avg", "median"                                        )
       
       
      #initialisation
      @logExceptions
      def __init__(self, *params, **paramDict):
          """
              Just positional parameters (forwarded to the constructor of 'EnhList') and the following keyword
              parameters are valid:
              
              'elemTypesT'               #list elements just can be of types which are in this tuple - otherwise an exception is raised; 'None' means: all types are allowed.
              'lockTypeS'                #can either be "mt_blocking", "mp_blocking", "mt_semi_blocking", "mp_semi_blocking" or "mp_semi_blocking" - were 'mt' stands for a multi threading and 'mp' for a multi processing lock.
              'timeoutMsF'               #just valid if a 'semi_blocking' lock is chosen
              'pollIntervalRangeMsT'     #just valid if a 'semi_blocking' lock is chosen
             
              If no 'lockTypeS' is given, 'BlockingMutex("mp_blocking")' is used as a default. For further 
              informations have a look at the doc string of 'SecList'.
          """
          
          ### init the context variable ###
          self._inWithContextB = False
           
          ### create the internal lock ###
          #lockParamDict: ignore keys from paramDict, 
          #which aren't valid keyword parameter keys for 'SemiBlockingMutex(...)'
          lockParamDict = { key: paramDict[key] for key in ('lockTypeS', 'timeoutMsF', 'pollIntervalRangeMsT') \
                            if key in paramDict.keys()                                                         }
                    
          #select lock type
          if    ("lockTypeS"     in lockParamDict.keys()) and (lockParamDict["lockTypeS"] == "mt_blocking"):
                self._lock = BlockingMutex("mt_blocking")
                
          elif  ("lockTypeS" not in lockParamDict.keys()) or (lockParamDict["lockTypeS"] == "mp_blocking"):
                #thus the default!
                self._lock = BlockingMutex("mp_blocking")
                
          else:
                self._lock = SemiBlockingMutex( **lockParamDict )
                
          ### call parent-s constructor ###
          EnhList.__init__( self, *params, **paramDict )     #just takes positional parameters and keyword parameter 
                                                             #'elemTypesT' into account, ignores all others
          
          
      ### create wrapper methods ###
      for methodNameS in lockedMethodsT:
          exec( """@logExceptions
def {0}(self, *params, **paramDict):
    " Wraps '{0}' of 'EnhList' with a lock-acquire/lock-release (using 'with self._lock:...'). "
      
    #secure access
    if    not self._inWithContextB:
          with self._lock:
               retVal = getattr( EnhList, "{0}" )(self, *params, **paramDict)

    else:
          retVal = getattr( EnhList, "{0}" )(self, *params, **paramDict)
          
    #ensure that return value is a 'SecList' - if a list at all
    if isinstance(retVal, list) and (not isinstance(retVal, SecList)):
       retVal                  = SecList( retVal, elemTypesT=self._elemTypesT )
       retVal._lock._enterCntI = self._lock._enterCntI
       retVal._lock._exitCntI  = self._lock._exitCntI
       
    #return value
    return retVal
                """.format(methodNameS) )
                
      del methodNameS
          
          
      #method called when entering a 'with' block
      @logExceptions
      def __enter__(self):
          """ With the 'with' statement a lock context is entered. """
          
          self._inWithContextB = True
          
          return self._lock.__enter__()
          
          
      #method called when exiting a 'with' block
      @logExceptions
      def __exit__(self, *exception):
          """ Leave the lock context. """
          
          self._inWithContextB = False
          
          return self._lock.__exit__(*exception)
                      
            
      #test thread-safety
      @classmethod
      @muteLogging
      def _testThreadSafety(self):
          """ Test whether SecList can be used thread-safe. """
          
          print ( "Testing Thread-Safety (needs a little time) ..." )
   
          def lockTest(threadIndexI, sL, numberOfElemsI=1000):
              """ Thread function - run by several threads in parallel. """    
              global elem
              
              #a 'define'
              numberOfElemsI = 1000
              
              #create a list of indices with random order
              baseL          = list(range(1,numberOfElemsI))
              Random_shuffle(baseL)
              
              #list for comparison
              cmpL = EnhList()
              
              #push elements into sL
              for element in baseL:
                  #identity function with high CPU effort
                  currO = TestO( threadIndexI, Math_factorial(element) / Math_factorial(element-1) )
                  
                  #this is a first secured (thread-safe) operation
                  sL.push( currO )
                       
              #pop elements from sL
              for indexI in range(1,numberOfElemsI):
                  #pop elements in order - this is a second secured (thread-safe) operation
                  popped = sL.pop((elem.a == threadIndexI) & (elem.b <= indexI))
                  
                  #check whether popped element is OK
                  if (len(popped) != 1) or (not hasattr(popped[0], "b")) or (popped[0].b != indexI):
                     raise Exception("Popped wrong element!") 
                     
                  #append to compare list
                  cmpL.push( popped[0] )
                     
              #check result
              cmpL.mapIf( lambda x: x.b )
              assert cmpL == list(range(1,numberOfElemsI))
              
             
          #the 'global' list for all threads
          sL     = SecList()
                       
          #create threads
          print("Test thread number 0 created")
          thread0        = Threading_Thread(target=lockTest, args=(0, sL))
          thread0.daemon = True
          print("Test thread number 1 created")
          thread1        = Threading_Thread(target=lockTest, args=(1, sL))
          thread1.daemon = True          
          print("Test thread number 2 created")
          thread2        = Threading_Thread(target=lockTest, args=(2, sL))
          thread2.daemon = True         
             
          #start threads
          thread0.start()
          thread1.start()
          thread2.start()
            
          #wait until threads finished
          thread0.join()
          thread1.join()
          thread2.join()
          
          print("All test threads finished.")
               
          print ( "...thread-Safety tested successfully!" )
            

      #selftest
      @classmethod
      @muteLogging
      def _selftest(cls):
          """ 
              Tests whether this class works as expected. It seems to, 
              if no exceptions are raised during the test.
          """
          
          print ( "Testing SecList..." )
          
          #create list using several parameters
          sL = SecList(1,3,5,7,9,11,13,15,17)
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL = SecList(1,3,5,7,9,11,13,15,17, elemTypesT=(int,float))
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          try:
                 sL = SecList(1,3,5,7,9,"a",13,15,17, elemTypesT=(int,float))
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          
          #create list using another list
          sL = SecList([1,3,5,7,9,11,13,15,17])
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          #create list using a tuple
          sL = SecList((1,3,5,7,9,11,13,15,17))
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL = SecList((1,3,5,7,9,11,13,15,17), elemTypesT=(int,float))
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL == [1,3,5,7,9,11,13,15,17]
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1          
          
          try:
                 sL = SecList((1,3,5,7,"a",11,13,15,17), elemTypesT=(int,float))
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          
          #get item using an index
          sL = SecList([1,3,5,7,9,11,13,15,17])
          item = sL[2]                                #first locking
          assert item == 5
          assert sL == [1,3,5,7,9,11,13,15,17]        #second locking
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          item = sL[2]                                #first locking
          assert item == 5
          assert sL == [1,3,5,7,9,11,13,15,17]        #second locking
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #get single item using a condition
          sL = SecList([1,3,5,7,9,11,13,15,17])
          item = sL[(elem > 5) & (elem < 11), single] #first lock
          assert sL == [1,3,5,7,9,11,13,15,17]        #second lock
          assert sL._elemTypesT == None
          assert item == 7
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          item = sL[(elem > 5) & (elem < 11), single] #first lock
          assert sL == [1,3,5,7,9,11,13,15,17]        #second lock
          assert sL._elemTypesT == (int,float)
          assert item == 7
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2          
          
          #get several items using a condition
          sL = SecList([1,3,5,7,9,11,13,15,17])
          items = sL[(elem > 5) & (elem < 11), several] #first lock
          assert sL == [1,3,5,7,9,11,13,15,17]          #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert items == [7,9]
          assert isinstance(items, SecList)
          assert items._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          items = sL[(elem > 5) & (elem < 11), several]  #first lock
          assert sL == [1,3,5,7,9,11,13,15,17]           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert items == [7,9]
          assert isinstance(items, SecList)
          assert items._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #get slice
          sL = SecList([1,3,5,7,9,11,13,15,17])
          slicee = sL[3:5]                               #first lock
          assert slicee == [7,9]
          assert isinstance(slicee, SecList)
          assert slicee._elemTypesT == None
          assert sL == [1,3,5,7,9,11,13,15,17]           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          slicee = sL[3:5]                               #first lock
          assert slicee == [7,9]
          assert isinstance(slicee, SecList)
          assert slicee._elemTypesT == (int,float)
          assert sL == [1,3,5,7,9,11,13,15,17]           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17])
          slicee = sL[1:-1:2]                            #first lock
          assert slicee == [3,7,11,15]
          assert isinstance(slicee, SecList)
          assert slicee._elemTypesT == None
          assert sL == [1,3,5,7,9,11,13,15,17]           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          slicee = sL[1:-1:2]                            #first lock
          assert slicee == [3,7,11,15]
          assert isinstance(slicee, SecList)
          assert slicee._elemTypesT == (int,float)
          assert sL == [1,3,5,7,9,11,13,15,17]           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2          

          #pop first
          sL = SecList([1,3,5,7,9,11,13,15,17])
          popped = sL.pop()                             #first lock
          assert popped == 1
          assert sL == [3,5,7,9,11,13,15,17]            #second lock
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          popped = sL.pop()                             #first lock
          assert popped == 1
          assert sL == [3,5,7,9,11,13,15,17]            #second lock
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #pop indexed
          sL = SecList([1,3,5,7,9,11,13,15,17])
          assert sL.pop(3) == 7                        #first lock
          assert sL == [1,3,5,9,11,13,15,17]           #ssecond lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          assert sL.pop(3) == 7                        #first lock
          assert sL == [1,3,5,9,11,13,15,17]           #ssecond lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #pop first meeting a condition
          sL = SecList([1,3,5,7,9,11,13,15,17])
          popped = sL.pop( (elem > 5) & (elem < 11), single )  #first lock
          assert popped == 7
          assert sL == [1,3,5,9,11,13,15,17]                   #second lock
          assert sL._elemTypesT == None
          assert isinstance(sL, SecList)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          popped = sL.pop( (elem > 5) & (elem < 11), single )  #first lock
          assert popped == 7
          assert sL == [1,3,5,9,11,13,15,17]                   #second lock
          assert sL._elemTypesT == (int,float)
          assert isinstance(sL, SecList)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #pop all meeting a condition
          sL = SecList([1,3,5,7,9,11,13,15,17])
          popped = sL.pop( (elem > 11) & (elem < 17), several ) #first lock
          assert popped == [13,15]
          assert isinstance(popped, SecList)
          assert popped._elemTypesT == None
          assert sL == [1,3,5,7,9,11,17]                        #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          popped = sL.pop( (elem > 11) & (elem < 17), several ) #first lock
          assert popped == [13,15]
          assert isinstance(popped, SecList)
          assert popped._elemTypesT == (int,float)
          assert sL == [1,3,5,7,9,11,17]                        #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          #push single
          sL = SecList([1,3,5,7,9,11,13,15,17])
          pushed = sL.push(19)                                  #first lock
          assert pushed == None
          assert sL == [1,3,5,7,9,11,13,15,17,19]               #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          pushed = sL.push(19)                                  #first lock
          assert pushed == None
          assert sL == [1,3,5,7,9,11,13,15,17,19]               #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          try:
                 pushed = sL.push("a")                                 #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
               
          assert sL == [1,3,5,7,9,11,13,15,17]                         #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #push several
          sL = SecList([1,3,5,7,9,11,13,15,17])
          pushed = sL.push(21,23,25)                                   #first lock
          assert pushed == None
          assert sL == [1,3,5,7,9,11,13,15,17,21,23,25]                #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          pushed = sL.push(21,23,25)                                   #first lock
          assert pushed == None
          assert sL == [1,3,5,7,9,11,13,15,17,21,23,25]                #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          try:
                  pushed = sL.push(21,"a",25)                          #first lock
                  assert False                                                                                         # pragma: no cover
          except  TypeMismatch:
                  pass
                
          assert pushed == None
          assert sL == [1,3,5,7,9,11,13,15,17]                         #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #set slice
          sL = SecList([1,3,5,7,9,11,13,15,17])
          sL[2:4] = [111,222]                                          #first lock
          assert sL == [1,3,111,222,9,11,13,15,17]                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          sL[2:4] = [111,222]                                          #first lock
          assert sL == [1,3,111,222,9,11,13,15,17]                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          try:
                 sL[2:4] = [111,"a"]                                   #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass

          assert sL == [1,3,5,7,9,11,13,15,17]                        #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17])
          sL[::2] = [111,222,333,444,555]                              #first lock
          assert sL == [111,3,222,7,333,11,444,15,555]                 #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          sL[::2] = [111,222,333,444,555]                              #first lock
          assert sL == [111,3,222,7,333,11,444,15,555]                 #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          try:
                 sL[::2] = [111,222,"aaa",444,555]                    #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
               
          assert sL == [1,3,5,7,9,11,13,15,17]                        #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #append
          sL = SecList([1,3,5,7,9,11,13,15,17])
          assert sL.append( 27 ) == None                              #first lock
          assert sL == [1,3,5,7,9,11,13,15,17,27]                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          assert sL.append( 27 ) == None                              #first lock
          assert sL == [1,3,5,7,9,11,13,15,17,27]                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          try:
                 assert sL.append( "a" ) == None                      #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
               
          assert sL == [1,3,5,7,9,11,13,15,17]                        #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #extend list
          sL = SecList([1,3,5,7,9,11,13,15,17])
          assert sL.extend([29,31]) == None                           #first lock
          assert sL == [1,3,5,7,9,11,13,15,17,29,31]                  #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float)) 
          assert sL.extend([29,31]) == None                             #first lock
          assert sL == [1,3,5,7,9,11,13,15,17,29,31]                    #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          try:
                 assert sL.extend([29,"a"]) == None                     #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
               
          assert sL == [1,3,5,7,9,11,13,15,17]                         #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #are all test
          sL = SecList([1,3,5,7,9,11,13,15,17])
          assert sL.areAll( elem > 0 ) == True                         #first lock
          assert sL.areAll( elem < 5 ) == False                        #second lock
          assert sL == [1,3,5,7,9,11,13,15,17]                         #third lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          assert sL.areAll( elem > 0 ) == True                         #first lock
          assert sL.areAll( elem < 5 ) == False                        #second lock
          assert sL == [1,3,5,7,9,11,13,15,17]                         #third lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          #count number of occurences
          sL = SecList([1,3,5,7,9,11,9,15,17])
          assert sL.count( 9 ) == 2                                    #first lock
          assert sL == [1,3,5,7,9,11,9,15,17]                          #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,9,15,17], elemTypesT=(int,float))
          assert sL.count( 9 ) == 2                                    #first lock
          assert sL == [1,3,5,7,9,11,9,15,17]                          #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2          

          #get index of an element
          sL = SecList([1,3,5,7,9,11,13,15,17])
          assert sL.index(9) == 4                                      #first lock
          assert sL == [1,3,5,7,9,11,13,15,17]                         #second lock
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          assert sL.index(9) == 4                                      #first lock
          assert sL == [1,3,5,7,9,11,13,15,17]                         #second lock
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          #insert in list
          sL = SecList([1,3,5,7,9,11,13,15,17])
          assert sL.insert(3, 333) == None                             #first lock
          assert sL == [1,3,5,333,7,9,11,13,15,17]                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          assert sL.insert(3, 333) == None                             #first lock
          assert sL == [1,3,5,333,7,9,11,13,15,17]                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15,17], elemTypesT=(int,float))
          try:
                 assert sL.insert(3, "a") == None                      #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
               
          assert sL == [1,3,5,7,9,11,13,15,17]                         #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          #map function on elements
          sL = SecList([1,3,5,7,9])
          assert sL.mapIf( lambda x: x * 2 ) == None                   #first lock
          assert sL == [2,6,10,14,18]                                  #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          assert sL.mapIf( lambda x: x * 2 ) == None                   #first lock
          assert sL == [2,6,10,14,18]                                  #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,str))
          try:
                 assert sL.mapIf( lambda x: x * 2.0 ) == None          #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass

          assert sL == [1,3,5,7,9]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,str)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2  
          
          #map function on elements if condition is met
          sL = SecList([1,3,5,7,9])
          assert sL.mapIf( lambda x: x / 3, elem % 3 == 0 ) == None    #first lock
          assert sL == [1,1,5,7,3]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          assert sL.mapIf( lambda x: x / 3, elem % 3 == 0 ) == None    #first lock
          assert sL == [1,1,5,7,3]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          try:
                 assert sL.mapIf( lambda x: "a"*x, elem % 3 == 0 ) == None    #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass               
          assert sL == [1,3,5,7,9]                                     #second lock
          
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #remove value
          sL = SecList([1,3,5,7,9,11,13])
          assert sL.remove( 7 ) == None                                #first lock
          assert sL == [1,3,5,9,11,13]                                 #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13], elemTypesT=(int,float))
          assert sL.remove( 7 ) == None                                #first lock
          assert sL == [1,3,5,9,11,13]                                 #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          #reverse element order
          sL = SecList([1,3,5,7,9])
          assert sL.reverse() == None                                  #first lock
          assert sL == [9,7,5,3,1]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          assert sL.reverse() == None                                  #first lock
          assert sL == [9,7,5,3,1]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #sort list
          sL = SecList([9,7,5,3,1])
          assert sL.sort() == None                                     #first lock
          assert sL == [1,3,5,7,9]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          assert sL.sort(reverse=True) == None                         #third lock
          assert sL == [9,7,5,3,1]                                     #fourth lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 4
          assert sL._lock._exitCntI  == 4
          
          sL = SecList([9,7,5,3,1], elemTypesT=(int,float))
          assert sL.sort() == None                                     #first lock
          assert sL == [1,3,5,7,9]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          assert sL.sort(reverse=True) == None                         #third lock
          assert sL == [9,7,5,3,1]                                     #fourth lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 4
          assert sL._lock._exitCntI  == 4
          
          #add list
          sL = SecList([1,3,5,7,9])
          nL = sL + [111,222]                                          #first lock
          assert nL == [1,3,5,7,9,111,222]
          assert isinstance(nL, SecList)
          assert nL._elemTypesT == None
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          assert sL == [1,3,5,7,9]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          sL + ["a", "b"]
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          nL = sL + [111,222]                                          #first lock
          assert nL == [1,3,5,7,9,111,222]
          assert isinstance(nL, SecList)
          assert nL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          assert sL == [1,3,5,7,9]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          try:
                 nL = None
                 nL = sL + [11, "b"]                                   #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          assert nL == None
          assert sL == [1,3,5,7,9]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9])
          nL = [111,222] + sL
          assert nL == [111,222,1,3,5,7,9]
          assert sL == [1,3,5,7,9]                                     #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          nL = [111,222] + sL
          assert nL == [111,222,1,3,5,7,9]
          assert sL == [1,3,5,7,9]                                     #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          #check whether list contains a value
          sL = SecList([1,3,5,7,9])
          assert (5  in sL) == True                                   #first lock
          assert (50 in sL) == False                                  #second lock
          assert ((elem > 5) in sL) == True                           #third lock
          assert (((elem > 3) & (elem < 7)) in sL) == True            #fourth lock
          assert ((elem > 50) in sL) == False                         #fifth lock
          assert (((elem > 30) & (elem < 70)) in sL) == False         #sixth lock
          assert sL == [1,3,5,7,9]                                    #seventh lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 7
          assert sL._lock._exitCntI  == 7
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          assert (5  in sL) == True                                   #first lock
          assert (50 in sL) == False                                  #second lock
          assert ((elem > 5) in sL) == True                           #third lock
          assert (((elem > 3) & (elem < 7)) in sL) == True            #fourth lock
          assert ((elem > 50) in sL) == False                         #fifth lock
          assert (((elem > 30) & (elem < 70)) in sL) == False         #sixth lock
          assert sL == [1,3,5,7,9]                                    #seventh lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 7
          assert sL._lock._exitCntI  == 7
          
          #delete single item
          sL = SecList([1,3,5,7,9])
          del sL[2]                                                   #first lock
          assert sL == [1,3,7,9]                                      #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          del sL[2]                                                   #first lock
          assert sL == [1,3,7,9]                                      #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #delete single item using condition
          sL = SecList([1,3,5,7,9])
          del sL[elem > 5, single]                                    #first lock
          assert sL == [1,3,5,9]                                      #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          del sL[elem > 5, single]                                    #first lock
          assert sL == [1,3,5,9]                                      #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #delete several items using condition
          sL = SecList([1,3,5,7,9])
          del sL[elem > 5]                                            #first lock
          assert sL == [1,3,5]                                        #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9], elemTypesT=(int,float))
          del sL[elem > 5]                                            #first lock
          assert sL == [1,3,5]                                        #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #delete slice
          sL = SecList([1,3,5,7,9,11,13,15])
          del sL[::2]                                                 #first lock
          assert sL == [3,7,11,15]                                    #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([1,3,5,7,9,11,13,15], elemTypesT=(int,float))
          del sL[::2]                                                 #first lock
          assert sL == [3,7,11,15]                                    #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          #string/display conversion
          sL = SecList([3,7,11,15])
          out1S = "test: {0}".format(sL)                               #first lock
          out2S = "test: %s" % sL                                      #second lock
          out3S = "test: " + repr(sL)                                  #third lock
          out4S = "test: " + str(sL)                                   #fourth lock
          assert (out1S == out2S == out3S == out4S) == True
          assert sL == [3,7,11,15]                                     #fifth lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 5
          assert sL._lock._exitCntI  == 5
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          out1S = "test: {0}".format(sL)                               #first lock
          out2S = "test: %s" % sL                                      #second lock
          out3S = "test: " + repr(sL)                                  #third lock
          out4S = "test: " + str(sL)                                   #fourth lock
          assert (out1S == out2S == out3S == out4S) == True
          assert sL == [3,7,11,15]                                     #fifth lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 5
          assert sL._lock._exitCntI  == 5
          
          #concatenate
          sL = SecList([3,7,11,15])
          sL += [101,102]                                              #first lock
          assert sL == [3,7,11,15,101,102]                             #second lock
          assert sL._elemTypesT == None
          assert isinstance(sL, SecList)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          sL += [101,102]                                              #first lock
          assert sL == [3,7,11,15,101,102]                             #second lock
          assert sL._elemTypesT == (int,float)
          assert isinstance(sL, SecList)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          try:
                 sL += [17, "b"]                                       #first lock
          except TypeMismatch:
                 pass
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #in-place multiply
          sL = SecList([3,7,11,15])
          sL *= 2                                                      #first lock
          assert sL == [3,7,11,15,3,7,11,15]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          sL *= 2                                                      #first lock
          assert sL == [3,7,11,15,3,7,11,15]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #get number of elements
          sL = SecList([3,7,11,15])
          noes = len(sL)                                               #first lock
          assert noes == 4
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          noes = len(sL)                                               #first lock
          assert noes == 4
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #multiply
          sL = SecList([3,7,11,15])
          nL = sL * 2                                                  #first lock
          assert nL == [3,7,11,15,3,7,11,15]
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(nL, SecList)
          assert nL._elemTypesT == None
          assert isinstance(sL, SecList)          
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          nL = sL * 2                                                  #first lock
          assert nL == [3,7,11,15,3,7,11,15]
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(nL, SecList)
          assert nL._elemTypesT == (int,float)
          assert isinstance(sL, SecList)          
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #set item
          sL = SecList([3,7,11,15])
          sL[2]  = 75                                                  #first lock
          assert sL == [3,7,75,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          sL[2] += 1                                                   #third & fourth lock
          assert sL == [3,7,76,15]                                     #fifth lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          sL[2] -= 2                                                   #6th & 7th lock
          assert sL == [3,7,74,15]                                     #8th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          sL[2] *= 2                                                   #9th & 10th lock
          assert sL == [3,7,148,15]                                    #11th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          sL[2] /= 2                                                   #12th & 13th lock
          assert sL == [3,7,74,15]                                     #14th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          sL[2] //= 2                                                  #15th & 16th lock
          assert sL == [3,7,37,15]                                     #17th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          sL[2] %= 3                                                   #18th & 19th lock
          assert sL == [3,7,1,15]                                      #20th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          sL[2]   = 2                                                  #21th lock
          sL[2] **= 3                                                  #22th & 23th lock
          assert sL == [3,7,8,15]                                      #24th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 24
          assert sL._lock._exitCntI  == 24
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          sL[2]  = 75                                                  #first lock
          assert sL == [3,7,75,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          sL[2] += 1                                                   #third & fourth lock
          assert sL == [3,7,76,15]                                     #fifth lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          sL[2] -= 2                                                   #6th & 7th lock
          assert sL == [3,7,74,15]                                     #8th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          sL[2] *= 2                                                   #9th & 10th lock
          assert sL == [3,7,148,15]                                    #11th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          sL[2] /= 2                                                   #12th & 13th lock
          assert sL == [3,7,74,15]                                     #14th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          sL[2] //= 2                                                  #15th & 16th lock
          assert sL == [3,7,37,15]                                     #17th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          sL[2] %= 3                                                   #18th & 19th lock
          assert sL == [3,7,1,15]                                      #20th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          sL[2]   = 2                                                  #21th lock
          sL[2] **= 3                                                  #22th & 23th lock
          assert sL == [3,7,8,15]                                      #24th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 24
          assert sL._lock._exitCntI  == 24
          
          sL = SecList([3,7,11,15], elemTypesT=(int,str))
          try:
                 sL[2]  = 75.1                                         #first lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,str)
          try:
                 sL[2] += 1.1                                          #third & fourth lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          assert sL == [3,7,11,15]                                     #fifth lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,str)
          try:
                 sL[2] -= 2.1                                          #6th & 7th lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          assert sL == [3,7,11,15]                                     #8th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,str)
          try:
                 sL[2] *= 2.1                                          #9th & 10th lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          assert sL == [3,7,11,15]                                     #11th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,str)
          try:
                 sL[2] /= 2.1                                          #12th & 13th lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          assert sL == [3,7,11,15]                                     #14th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,str)
          sL[2]   = 2                                                  #15th lock
          try:
                 sL[2] **= 3.1                                         #16th & 17th lock
                 assert False                                                                                          # pragma: no cover
          except TypeMismatch:
                 pass
          assert sL == [3,7,2,15]                                      #18th lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,str)
          assert sL._lock._enterCntI == 18
          assert sL._lock._exitCntI  == 18
          
          #right multiply
          sL = SecList([3,7,11,15])
          nL = 2 * sL                                                  #first lock
          assert nL == [3,7,11,15,3,7,11,15]
          assert isinstance(nL, SecList)
          assert nL._elemTypesT == None
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          nL = 2 * sL                                                  #first lock
          assert nL == [3,7,11,15,3,7,11,15]
          assert isinstance(nL, SecList)
          assert nL._elemTypesT == (int, float)
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #get size in memory
          assert isinstance(sL.__sizeof__(), int) == True
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3

          #external functions do not trigger a lock context
          #that's why a 'with' is necessary here
          sL = SecList([3,7,11,15])
          with sL:                                                     #first lock
               reduced = reduce(lambda x,y: x+y, sL)
               summed  = sum(sL)
          assert reduced == summed == 36
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None                     
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          with sL:                                                     #first lock
               reduced = reduce(lambda x,y: x+y, sL)
               summed  = sum(sL)
          assert reduced == summed == 36
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)                     
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #comparison - not equal
          sL = SecList([3,7,11,15])
          assert (sL != []) == True                                    #first lock
          assert (sL != [3,7,11,15]) == False                          #second lock
          assert sL == [3,7,11,15]                                     #third lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          assert (sL != []) == True                                    #first lock
          assert (sL != [3,7,11,15]) == False                          #second lock
          assert sL == [3,7,11,15]                                     #third lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          #iterator protocol - list comprehension
          sL = SecList([3,7,11,15])
          with sL:                                                     #first lock
               nL = [element for element in sL if element > 10]
          assert nL == [11,15]
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          with sL:                                                     #first lock
               nL = [element for element in sL if element > 10]
          assert nL == [11,15]
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #iterator protocol - tuple comprehension
          sL = SecList([3,7,11,15])
          with sL:                                                     #first lock
               nL = (element for element in sL if element > 10)
          assert tuple(nL) == (11,15)
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          with sL:                                                     #first lock
               nL = (element for element in sL if element > 10)
          assert tuple(nL) == (11,15)
          assert sL == [3,7,11,15]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #iterator protocol - next
          sL = SecList([3,7,11,15])
          nL = SecList()
          iterator = iter(sL)
          try:
                 with sL:                                           #first lock
                      while True:
                            if    isPy2() == True:
                                  nL.push( iterator.next() )
                            else:
                                  nL.push( iterator.__next__() )
                        
          except StopIteration:
                 pass
          assert sL == nL == [3,7,11,15]                            #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert isinstance(nL, SecList)
          assert nL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          nL = SecList(elemTypesT=(int,float))
          iterator = iter(sL)
          try:
                 with sL:                                           #first lock
                      while True:
                            if    isPy2() == True:
                                  nL.push( iterator.next() )
                            else:
                                  nL.push( iterator.__next__() )
                        
          except StopIteration:
                 pass
          assert sL == nL == [3,7,11,15]                            #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert isinstance(nL, SecList)
          assert nL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #min, max
          sL = SecList([3,7,11,15])
          assert min(sL) == 3
          assert max(sL) == 15
          assert sL == [3,7,11,15]                                  #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          assert min(sL) == 3
          assert max(sL) == 15
          assert sL == [3,7,11,15]                                  #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1

          #for ... in ... loop
          sL = SecList([3,7,11,15])
          summed = 0
          with sL:                                                  #first lock
               for element in sL:
                   summed += element
          assert summed == sum(sL) == 36
          assert sL == [3,7,11,15]                                  #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,7,11,15], elemTypesT=(int,float))
          summed = 0
          with sL:                                                  #first lock
               for element in sL:
                   summed += element
          assert summed == sum(sL) == 36
          assert sL == [3,7,11,15]                                  #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #pickle
          sL = SecList([3,7,11,15])
          pickled   = Pickle_dumps(list(sL))                        #first lock
          unpickled = Pickle_loads(pickled)
          assert unpickled == sL                                    #second lock
          if isPy2() == True:
                assert sL._lock._enterCntI == 2
                assert sL._lock._exitCntI  == 2
          else:
                assert sL._lock._enterCntI == 3
                assert sL._lock._exitCntI  == 3            
          
          #map
          sL = SecList([3.1,7.1,11.1,15.1])
          mapped = SecList(map(int, sL))                            #first lock
          assert mapped == [3,7,11,15]
          assert isinstance(mapped, SecList)
          assert mapped._elemTypesT == None
          assert sL == [3.1,7.1,11.1,15.1]                          #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          if isPy2() == True:
                assert sL._lock._enterCntI == 2
                assert sL._lock._exitCntI  == 2
          else:
                assert sL._lock._enterCntI == 1
                assert sL._lock._exitCntI  == 1 
          
          sL = SecList([3.1,7.1,11.1,15.1], elemTypesT=(int,float))
          mapped = SecList(map(int, sL), elemTypesT=(int,float))    #first lock
          assert mapped == [3,7,11,15]
          assert isinstance(mapped, SecList)
          assert mapped._elemTypesT == (int,float)
          assert sL == [3.1,7.1,11.1,15.1]                          #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          if isPy2() == True:
                assert sL._lock._enterCntI == 2
                assert sL._lock._exitCntI  == 2
          else:
                assert sL._lock._enterCntI == 1
                assert sL._lock._exitCntI  == 1 
          
          #reverse
          sL = SecList([3,5,7,11,13,15])
          sL.reverse()                                              #first lock
          assert sL == [15,13,11,7,5,3]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,5,7,11,13,15], elemTypesT=(int,float))
          sL.reverse()                                              #first lock
          assert sL == [15,13,11,7,5,3]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #reversed
          sL = SecList([3,5,7,11,13,15])
          nL = list(reversed(sL))                                   #first lock
          assert nL == [15,13,11,7,5,3]                             
          assert sL == [3,5,7,11,13,15]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([3,5,7,11,13,15], elemTypesT=(int,float))
          nL = list(reversed(sL))                                   #first lock
          assert nL == [15,13,11,7,5,3]                             
          assert sL == [3,5,7,11,13,15]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          ###applyMapIf
          #(lambda) function parameter
          sL = SecList(( [index, index] for index in range(3) ))
          sL.applyMapIf( lambda x: list.__setitem__(x, 1, 111) )    #first lock
          sL.applyMapIf( lambda x: x.append(222) )                  #second lock
          assert sL == [[0, 111, 222], [1, 111, 222], [2, 111, 222]] #third lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          #(lambda) function parameter - in type check mode
          sL = SecList(( [index, index] for index in range(3) ), elemTypesT=(tuple,list))
          sL.applyMapIf( lambda x: list.__setitem__(x, 1, 111) )
          sL.applyMapIf( lambda x: x.append(222) )
          assert sL == [[0, 111, 222], [1, 111, 222], [2, 111, 222]]
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (tuple,list)
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
                             
          ### with condition ###
          #(lambda) function parameter
          sL = SecList(( [index, index] for index in range(5) ))
          sL.applyMapIf( lambda x: list.__setitem__(x, 1, 111), lambda x: x[0] % 2 == 0 )
          sL.applyMapIf( lambda x: x.append(222), lambda x: x[0] % 2 == 1 )
          assert sL == [[0, 111], [1, 1, 222], [2, 111], [3, 3, 222], [4, 111]] 
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          #(lambda) function parameter - in type check mode
          sL = SecList(( [index, index] for index in range(5) ), elemTypesT=(tuple,list))
          sL.applyMapIf( lambda x: list.__setitem__(x, 1, 111), lambda x: x[0] % 2 == 0 )
          sL.applyMapIf( lambda x: x.append(222), lambda x: x[0] % 2 == 1 )
          assert sL == [[0, 111], [1, 1, 222], [2, 111], [3, 3, 222], [4, 111]] 
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (tuple,list)
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          #.min
          sL = SecList([11,13,15,3,5,7])
          sL.min() == 3                                             #first lock
          assert sL == [11,13,15,3,5,7]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([11,13,15,3,5,7], elemTypesT=(int,float))
          sL.min() == 3                                             #first lock
          assert sL == [11,13,15,3,5,7]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #.max
          sL = SecList([11,13,15,3,5,7])
          sL.max() == 15                                            #first lock
          assert sL == [11,13,15,3,5,7]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([11,13,15,3,5,7], elemTypesT=(int,float))
          sL.max() == 15                                            #first lock
          assert sL == [11,13,15,3,5,7]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #.sum
          sL = SecList([11,13,15,3,5,7])
          sL.sum() == 54                                            #first lock
          assert sL == [11,13,15,3,5,7]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([11,13,15,3,5,7], elemTypesT=(int,float))
          sL.sum() == 54                                            #first lock
          assert sL == [11,13,15,3,5,7]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #.avg
          sL = SecList([11,13,15,3,5,7])
          sL.avg() == 9                                             #first lock
          assert sL == [11,13,15,3,5,7]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([11,13,15,3,5,7], elemTypesT=(int,float))
          sL.avg() == 9                                             #first lock
          assert sL == [11,13,15,3,5,7]                             #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #.median
          sL = SecList([11])
          sL.median() == 11                                          #first lock
          assert sL == [11]                                          #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([11,13])
          sL.median() == 12                                          #first lock
          assert sL == [11,13]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([11,13,15])
          sL.median() == 13                                          #first lock
          assert sL == [11,13,15]                                    #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([11], elemTypesT=(int,float))
          sL.median() == 11                                          #first lock
          assert sL == [11]                                          #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([11,13], elemTypesT=(int,float))
          sL.median() == 12                                          #first lock
          assert sL == [11,13]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL = SecList([11,13,15], elemTypesT=(int,float))
          sL.median() == 13                                          #first lock
          assert sL == [11,13,15]                                    #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          ### with context for unsafe operations ###
          #inplace arithmetics without 'with'
          sL         = SecList(1,3,5)
          sL[1]     += 1                                             #first & second lock
          assert sL == [1,4,5]                                       #third lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          sL[1]     += 1                                             #first & second lock
          assert sL == [1,4,5]                                       #third lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          #inplace arithmetics with 'with'
          sL         = SecList(1,3,5)
          with sL:                                                   #first lock
               sL[1]     += 1                                        
          assert sL == [1,4,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          with sL:                                                   #first lock
               sL[1]     += 1                                        
          assert sL == [1,4,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          with sL:                                                   #first lock
               try:
                      sL[1]     += 1.1
                      assert False                                                                                          # pragma: no cover
               except TypeMismatch:
                      pass
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #reduce without 'with'
          sL         = SecList(1,3,5)
          reduce(lambda x,y: x+y, sL) == 9
          assert sL == [1,3,5]                                       #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          reduce(lambda x,y: x+y, sL) == 9
          assert sL == [1,3,5]                                       #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          #reduce with 'with'
          sL         = SecList(1,3,5)
          with sL:                                                   #first lock
               reduce(lambda x,y: x+y, sL) == 9
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          with sL:                                                   #first lock
               reduce(lambda x,y: x+y, sL) == 9                                       
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,"a",5, elemTypesT=(int,str))
          try:
                  with sL:                                           #first lock
                       reduce(lambda x,y: x+y, sL) == 9                                       
          except:
                  pass
          assert sL == [1,"a",5]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #list comprehension without 'with'
          sL         = SecList(1,3,5)
          nL         = [ (el*2) for el in sL if el > 2 ]
          assert nL == [6,10]
          assert not isinstance(nL, SecList)
          assert sL == [1,3,5]                                       #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          nL         = [ (el*2) for el in sL if el > 2 ]
          assert nL == [6,10]
          assert not isinstance(nL, SecList)
          assert sL == [1,3,5]                                       #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          #list comprehension with 'with'
          sL         = SecList(1,3,5)
          with sL:                                                   #first lock
               nL    = [ (el*2) for el in sL if el > 2 ]
          assert nL == [6,10]
          assert not isinstance(nL, SecList)
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          with sL:                                                   #first lock
               nL    = [ (el*2) for el in sL if el > 2 ]
          assert nL == [6,10]
          assert not isinstance(nL, SecList)
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          try:
                  with sL:                                          #first lock
                       nL    = [ (el*2) for el in sL if el > 2 ]
          except:
                  pass
          assert sL == [1,3,5]                                      #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          
          assert sL[0] == 1                                        #just to be sure, that list is not deadlock yet
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          #tuple comprehension without 'with'
          sL         = SecList(1,3,5)
          nL         = ( (el*2) for el in sL if el > 2 )
          assert list(nL) == [6,10]
          assert sL == [1,3,5]                                       #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          nL         = ( (el*2) for el in sL if el > 2 )
          assert list(nL) == [6,10]
          assert sL == [1,3,5]                                       #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          #list comprehension with 'with'
          sL         = SecList(1,3,5)
          with sL:                                                   #first lock
               nL    = ( (el*2) for el in sL if el > 2 )
          assert list(nL) == [6,10]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          with sL:                                                   #first lock
               nL    = ( (el*2) for el in sL if el > 2 )
          assert list(nL) == [6,10]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,str))
          try:
                  with sL:                                          #first lock
                       nL    = ( (el*2) for el in sL if el > 2 )
          except:
                  pass
          assert list(nL) == [6,10]
          assert sL == [1,3,5]                                      #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          
          assert sL[0] == 1                                        #just to be sure, that list is not deadlock yet
          assert sL._lock._enterCntI == 3
          assert sL._lock._exitCntI  == 3
          
          #map without 'with'
          sL         = SecList(1,3,5)
          nL         = map(lambda x:x+1, sL)                         #first lock
          assert list(nL) == [2,4,6]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          if isPy2() == True:
                assert sL._lock._enterCntI == 2
                assert sL._lock._exitCntI  == 2
          else:
                assert sL._lock._enterCntI == 1
                assert sL._lock._exitCntI  == 1 
          
          sL         = SecList(1,3,5, elemTypesT=(int,float))
          nL         = map(lambda x:x+1, sL)                         #first lock
          assert list(nL) == [2,4,6]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._inWithContextB  == False
          if isPy2() == True:
                assert sL._lock._enterCntI == 2
                assert sL._lock._exitCntI  == 2
          else:
                assert sL._lock._enterCntI == 1
                assert sL._lock._exitCntI  == 1 
          
          #map with 'with'
          sL         = SecList(1,3,5)
          with sL:                                                   #first lock
               nL    = map(lambda x:x+1, sL)
          assert list(nL) == [2,4,6]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,float))
          with sL:                                                   #first lock
               nL    = map(lambda x:x+1, sL)
          assert list(nL) == [2,4,6]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,"a",5, elemTypesT=(int,str))
          try:
                  with sL:                                           #first lock
                       nL    = map(lambda x:x+1, sL)
          except:
                  pass
          assert sL == [1,"a",5]                                     #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,str)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          #sorted without 'with'
          sL         = SecList(1,3,5)
          nL         = sorted(sL, reverse=True)                      #first lock
          assert list(nL) == [5,3,1]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,float))
          nL         = sorted(sL, reverse=True)                      #first lock
          assert list(nL) == [5,3,1]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #sorted with 'with'
          sL         = SecList(1,3,5)
          with sL:                                                   #first lock
               nL    = sorted(sL, reverse=True)
          assert list(nL) == [5,3,1]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,float))
          with sL:                                                   #first lock
               nL    = sorted(sL, reverse=True)
          assert list(nL) == [5,3,1]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #reversed without 'with'
          sL         = SecList(1,3,5)
          nL         = reversed(sL)                                  #first lock
          assert list(nL) == [5,3,1]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,float))
          nL         = reversed(sL)                                  #first lock
          assert list(nL) == [5,3,1]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #reversed with 'with'
          sL         = SecList(1,3,5)
          with sL:                                                   #first lock
               nL    = reversed(sL)
          assert list(nL) == [5,3,1]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5, elemTypesT=(int,float))
          with sL:                                                   #first lock
               nL    = reversed(sL)
          assert list(nL) == [5,3,1]
          assert sL == [1,3,5]                                       #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #all without 'with'
          sL         = SecList(True, True, True)
          assert all(sL)                                             
          assert sL == [True, True, True]                            #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL         = SecList(True, False, True, elemTypesT=(int,bool))
          assert not all(sL)                                         
          assert sL == [True, False, True]                           #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,bool)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          #all with 'with'
          sL         = SecList(True, True, True)
          with sL:                                                   #first lock
               assert all(sL)
          assert sL == [True, True, True]                            #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(True, False, True, elemTypesT=(int,bool))
          with sL:                                                   #first lock
               assert not all(sL)
          assert sL == [True, False, True]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,bool)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #any without 'with'
          sL         = SecList(False,True,False)
          assert any(sL)                                             
          assert sL == [False,True,False]                            #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          sL         = SecList(False,False,False, elemTypesT=(int,bool))
          assert not any(sL)                                         
          assert sL == [False,False,False]                           #first lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,bool)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 1
          assert sL._lock._exitCntI  == 1
          
          #any with 'with'
          sL         = SecList(False,True,False)
          with sL:                                                   #first lock
               assert any(sL)
          assert sL == [False,True,False]                            #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(False,False,False, elemTypesT=(int,bool))
          with sL:                                                   #first lock
               assert not any(sL)
          assert sL == [False,False,False]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,bool)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          #filter without 'with'
          sL         = SecList(1,3,5,7,9)
          assert list(filter(lambda x: x > 4, sL)) == [5,7,9]       #first lock
          assert sL == [1,3,5,7,9]                                  #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          if isPy2() == True:
                assert sL._lock._enterCntI == 2
                assert sL._lock._exitCntI  == 2
          else:
                assert sL._lock._enterCntI == 1
                assert sL._lock._exitCntI  == 1 
          
          sL         = SecList(1,3,5,7,9, elemTypesT=(int,float))
          assert list(filter(lambda x: x > 4, sL)) == [5,7,9]      #first lock
          assert sL == [1,3,5,7,9]                                 #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._inWithContextB  == False
          if isPy2() == True:
                assert sL._lock._enterCntI == 2
                assert sL._lock._exitCntI  == 2
          else:
                assert sL._lock._enterCntI == 1
                assert sL._lock._exitCntI  == 1 
          
          #filter with 'with'
          sL         = SecList(1,3,5,7,9)
          with sL:                                            #first lock
               assert list(filter(lambda x: x > 4, sL)) == [5,7,9]
          assert sL == [1,3,5,7,9]                            #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          sL         = SecList(1,3,5,7,9, elemTypesT=(int,bool))
          with sL:                                           #first lock
               assert list(filter(lambda x: x > 4, sL)) == [5,7,9]
          assert sL == [1,3,5,7,9]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,bool)
          assert sL._inWithContextB  == False
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          if isPy2() == True:
             #apply without 'with'
             sL         = SecList(1,3,5,3,1)
             assert apply(max, sL) == 5                          #first lock
             assert sL == [1,3,5,3,1]                            #second lock
             assert isinstance(sL, SecList)
             assert sL._elemTypesT      == None
             assert sL._inWithContextB  == False
             assert sL._lock._enterCntI == 2
             assert sL._lock._exitCntI  == 2
            
             sL         = SecList(1,3,5,3,1, elemTypesT=(int,float))
             assert apply(max, sL) == 5                          #first lock
             assert sL == [1,3,5,3,1]                            #second lock
             assert isinstance(sL, SecList)
             assert sL._elemTypesT      == (int,float)
             assert sL._inWithContextB  == False
             assert sL._lock._enterCntI == 2
             assert sL._lock._exitCntI  == 2
            
             #apply with 'with'
             sL         = SecList(1,3,5,3,1)
             with sL:                                            #first lock
                 assert apply(max, sL) == 5                     
             assert sL == [1,3,5,3,1]                            #second lock
             assert isinstance(sL, SecList)
             assert sL._elemTypesT      == None
             assert sL._inWithContextB  == False
             assert sL._lock._enterCntI == 2
             assert sL._lock._exitCntI  == 2
            
             sL         = SecList(1,3,5,3,1, elemTypesT=(int,bool))
             with sL:                                           #first lock
                 assert apply(max, sL) == 5                     
             assert sL == [1,3,5,3,1]                           #second lock
             assert isinstance(sL, SecList)
             assert sL._elemTypesT      == (int,bool)
             assert sL._inWithContextB  == False
             assert sL._lock._enterCntI == 2
             assert sL._lock._exitCntI  == 2
          
          #test, whether all returned lists are SecList-s
          sL = SecList(1,3,5,7,9,11,13)
          assert isinstance( sL,               SecList )
          assert isinstance( sL[2:4],          SecList )
          assert isinstance( sL[2::2],         SecList )
          assert isinstance( sL + [15,17],     SecList )
          assert isinstance( sL * 3,           SecList )
          assert isinstance( 3 * sL,           SecList )
          assert isinstance( sL[elem > 3],     SecList )
          assert isinstance( sL.pop(elem > 3), SecList)
          
          #test mutex parameters
          sL = SecList(1,3,5,7,9,11,13)
          assert isinstance(sL._lock, BlockingMutex)
          
          sL = SecList(1,3,5,7,9,11,13, lockTypeS="mt_blocking")
          assert isinstance(sL._lock, BlockingMutex)
          
          sL = SecList(1,3,5,7,9,11,13, lockTypeS="mp_blocking")
          assert isinstance(sL._lock, BlockingMutex)
          
          sL = SecList(1,3,5,7,9,11,13, lockTypeS="mt_semi_blocking")
          assert isinstance(sL._lock, SemiBlockingMutex)
          
          sL = SecList(1,3,5,7,9,11,13, lockTypeS="mt_semi_blocking")
          assert isinstance(sL._lock, SemiBlockingMutex)
          
          sL = SecList(1,3,5,7,9,11,13, lockTypeS="mt_semi_blocking", timeoutMsF=123, pollIntervalRangeMsT=(0.12345, 1.2345))
          assert isinstance(sL._lock, SemiBlockingMutex)
          assert sL._lock._timeoutMsF           == 123
          assert sL._lock._pollIntervalRangeMsT == (0.12345, 1.2345)
          
          sL = SecList(1,3,5,7,9,11,13, lockTypeS="mp_semi_blocking", timeoutMsF=123, pollIntervalRangeMsT=(0.12345, 1.2345))
          assert isinstance(sL._lock, SemiBlockingMutex)
          assert sL._lock._timeoutMsF           == 123
          assert sL._lock._pollIntervalRangeMsT == (0.12345, 1.2345)
          
          #set item
          sL         = SecList(1,3,5,7,9,11)
          sL[2]      = 55                                        #first lock 
          assert sL == [1,3,55,7,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          sL[2]      = "a"
          
          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          sL[2]      = 55                                        #first lock 
          assert sL == [1,3,55,7,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          try:
                 sL[2]      = "a"
                 assert False                                                                                          # pragma: no cover
                 
          except TypeMismatch:
                 pass
               
          #set slice
          sL         = SecList(1,3,5,7,9,11)
          sL[2:4]    = [55,77]                                    #first lock 
          assert sL == [1,3,55,77,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          sL[2]      = "a"
          
          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          sL[2:4]    = [55,77]                                    #first lock 
          assert sL == [1,3,55,77,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          try:
                 sL[2:4] = ["a","b"]
                 assert False                                                                                          # pragma: no cover
                 
          except TypeMismatch:
                 pass
               
          sL         = SecList(1,3,5,7,9,11)
          sL[1:5:2]  = [33,77]                                    #first lock 
          assert sL == [1,33,5,77,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          sL[2]      = "a"
          
          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          sL[1:5:2]  = [33,77]                                    #first lock 
          assert sL == [1,33,5,77,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          
          try:
                 sL[1:5:2] = ["a","b"]
                 assert False                                                                                          # pragma: no cover
                 
          except TypeMismatch:
                 pass

          #set item conditionally
          sL         = SecList(1,3,5,7,9,11)
          sL[ (elem > 3) & (elem < 9) ] = 222                     #first lock 
          assert sL == [1,3,222,222,9,11]                         #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          sL         = SecList(1,3,5,7,9,11)
          sL[ (elem > 3) & (elem < 9) ] = "a"

          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          sL[ (elem > 3) & (elem < 9) ] = 222                     #first lock 
          assert sL == [1,3,222,222,9,11]                         #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          try:
                 sL[ (elem > 3) & (elem < 9) ] = "a"
                 assert False                                                                                          # pragma: no cover
                 
          except TypeMismatch:
                 pass
               
          sL         = SecList(1,3,5,7,9,11)
          sL[ (elem > 3) & (elem < 9), single ] = 222             #first lock 
          assert sL == [1,3,222,7,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          sL         = SecList(1,3,5,7,9,11)
          sL[ (elem > 3) & (elem < 9), single ] = "a"

          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          sL[ (elem > 3) & (elem < 9), single ] = 222             #first lock 
          assert sL == [1,3,222,7,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          try:
                 sL[ (elem > 3) & (elem < 9), single ] = "a"
                 assert False                                                                                          # pragma: no cover
                 
          except TypeMismatch:
                 pass

          sL         = SecList(1,3,5,7,9,11)
          sL[ (elem == 3) | (elem == 9) ] = elem + 10             #first lock 
          assert sL == [1,13,5,7,19,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          sL[ (elem == 3) | (elem == 9) ] = elem * "a"
          
          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          sL[ (elem == 3) | (elem == 9) ] = elem + 10             #first lock 
          assert sL == [1,13,5,7,19,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          try:
                 sL[ (elem == 3) | (elem == 9) ] = elem * "a"
                 assert False                                                                                          # pragma: no cover
                 
          except TypeMismatch:
                 pass
               
          sL         = SecList(1,3,5,7,9,11)
          sL[ (elem == 3) | (elem == 9), single ] = elem + 10     #first lock 
          assert sL == [1,13,5,7,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2
          sL[ (elem == 3) | (elem == 9), single ] = elem * "a"
          
          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          sL[ (elem == 3) | (elem == 9), single ] = elem + 10     #first lock 
          assert sL == [1,13,5,7,9,11]                           #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (int,float)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          sL         = SecList(1,3,5,7,9,11, elemTypesT=(int,float))
          try:
                 sL[ (elem == 3) | (elem == 9), single ] = elem * "a"
                 assert False                                                                                          # pragma: no cover
                 
          except TypeMismatch:
                 pass

          sL         = SecList([1,1],[2,3],[3,5],[4,7])
          sL[ elem[0] % 2 == 0 ] = None                           #first lock 
          assert sL == [[1,1],None,[3,5],None]                    #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          sL         = SecList([1,1],[2,3],[3,5],[4,7], elemTypesT=(list,int))
          sL[ elem[0] % 2 == 0 ] = 0                             #first lock 
          assert sL == [[1,1],0,[3,5],0]                         #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (list,int)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          sL         = SecList([1,1],[2,3],[3,5],[4,7], elemTypesT=(list,int))
          try:
                 sL[ elem[0] % 2 == 0 ] = None
                 assert False                                                                                          # pragma: no cover
                 
          except TypeMismatch:
                 pass
               
          TmpT = Collections_namedtuple("TmpT", ("aaa","bbb"))
          sL         = SecList(TmpT(1,1),TmpT(2,3),TmpT(3,5),TmpT(4,7))
          sL[ elem.aaa % 2 == 0 ] = None                         #first lock 
          assert sL == [(1,1),None,(3,5),None]                   #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == None
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          sL         = SecList(TmpT(1,1),TmpT(2,3),TmpT(3,5),TmpT(4,7), elemTypesT=(tuple,int))
          sL[ elem.aaa % 2 == 0 ] = 0                            #first lock 
          assert sL == [(1,1),0,(3,5),0]                         #second lock
          assert isinstance(sL, SecList)
          assert sL._elemTypesT      == (tuple,int)
          assert sL._lock._enterCntI == 2
          assert sL._lock._exitCntI  == 2

          sL         = SecList(TmpT(1,1),TmpT(2,3),TmpT(3,5),TmpT(4,7), elemTypesT=(tuple,int))
          try:
                 sL[ elem.aaa % 2 == 0 ] = None
                 assert False                                                                                          # pragma: no cover
                 
          except TypeMismatch:
                 pass
               
          #test thread safety
          cls._testThreadSafety()
        
          print ( "...SecList tested successfully!" )
          
          
          
##################
# Box List Class #
##################
class BoxList(EnhList):
      """ 
          --- still UNDER CONSTRUCTION ---
          
          A BoxList is an EnhList with an additional method 'shiftPush' 
          and a belonging 'widthI'.
          
          It can be used to implement things alike 'sliding averages' and so on.
          As long as you just use 'shiftPush' to insert elements into self, the 
          number of elements won't exceed 'widthI' (the 'box width'). Have a look
          at the doc text of said 'self.shiftPush(...)' method and the following examples.
          
          examples for said ADDITIONAL capabilities (standard EnhList operations work too):
          
          BoxList( 5              )       ==> []
          BoxList( 5, (1,2,3)     )       ==> [1,2,3]
          BoxList( 5, [1,2,3,4,5] )       ==> [1,2,3,4,5]
          
          bL = BoxList( 5, [1,2,3,4,5] )                        #bL: [1,2,3,4,5]
          bL.shiftPush( 6 )               ==> [1]               #bL: [2,3,4,5,6]
          bL.shiftPush( 7,8,9 )           ==> [2,3,4]           #bL: [5,6,7,8,9]
      """
      
      widthI = None
      
      
      #initialisation
      @logExceptions
      def __init__(self, widthI, contentL=[]):
          """

          """
          
          #ensure, that parameter width is a compatible type (int or long or alike)
          #and init self.widthI accordingly
          if    not isinstance(widthI, (int, long)):
                self.widthI = long( widthI )
                assert self.widthI == widthI, \
                       "The parameter 'widthI' must either be an 'int', a 'long' or a type, " \
                       "which is losslessly convertible to 'long' (%s)!" % widthI
                       
          else:
                self.widthI = widthI


          #check type of parameter 'contentL'
          assert isinstance(contentL, (list, tuple)), \
                 "The parameter contentL either must be of type 'list' or 'tuple' (%s)!" % contentL
                 
          #check whether len(gth) of parameter 'contentL' fits to parameter 'widthI'
          assert len(contentL) <= self.widthI, \
                 "The number of elements of parameter 'contentL' " \
                 "must not exceed the (parameter) 'widthI' of the box (%d)!" % len(contentL)
          
          
          #call the __init__ of the parent 'list' class accordingly
          EnhList.__init__(self, contentL)
          
          
      #method testing __init__
      @classmethod
      @muteLogging
      def _initSelftest(cls):
          """ """
          
          print ( "Testing BoxList.__init__..." )
          
          ### no parameter ###
          try:
                 boxL = BoxList()
                 raise FatalError("unexpected")
                 
          except TypeError:
                 pass
          
          ### just the box width parameter ###
          #valid width parameters
          boxL = BoxList( 5 )
          assert boxL.widthI == 5
          boxL = BoxList( long(5) )
          assert boxL.widthI == 5
          
          #invalid width parameter
          try:
                 boxL = BoxList( 5.123 )
                 raise FatalError("unexpected")
                 
          except AssertionError:
                 pass
               
          ### width AND list elements parameters ###
          #valid parameter combination
          boxL = BoxList( 5, (1,3,5) )
          assert boxL.widthI == 5
          assert boxL        == [1,3,5]
          boxL = BoxList( long(5), [1,3,5] )
          assert boxL.widthI == 5
          assert boxL        == [1,3,5]          
          
          #invalid parameter combination
          try:
                 boxL = BoxList( 5, (1,3,5,7,9,11) )
                 raise FatalError("unexpected")
                 
          except AssertionError:
                 pass               

          print ( "...BoxList.__init__ tested sucessfully!" )
          
          
      #push element(s) to the end
      @logExceptions
      def shiftPush(self, *params):
          """
              'shiftPush' appends elements given as the parameters to the 
              end of the list. If the total number of elements of said list 
              after that exceeds 'self.widthI', all elements at the beginning
              of the list, which are too much, are popped and returned
              as a list; otherwise just None is returned.
              
              This method accepts no, one or several parameters (elements to 
              be appended).
          """
          
          #accept no, one or several parameters
          if    len(params) == 1:
                #one parameter
                EnhList.append( self, *params )
                
          else:
                #no or several parameters
                EnhList.extend( self, params )
                
          #delimit box width
          if    len(self) > self.widthI:
                #get elems to be popped
                if    isPy2() == True:
                      retL = EnhList.__getslice__(self, 0, len(self) - self.widthI)
                      EnhList.__delslice__(self, 0, len(self) - self.widthI)
                    
                else:
                      retL = EnhList.__getitem__(self, slice(0, len(self) - self.widthI, None))
                      EnhList.__delitem__(self, slice(0, len(self) - self.widthI, None))
                      
                return retL
                
          else:
                return None
                
                
      #method testing shiftPush
      @classmethod
      @muteLogging
      def _shiftPushSelftest(cls):
          """ """
          
          print ( "Testing BoxList.shiftPush..." )
          
          ### valid push-through-s ###
          #create empty list
          boxL = BoxList( 5 )
          assert len(boxL) == 0
          assert boxL == []
          
          #fill up list
          for elemI in range(1, 6):
              ret = boxL.shiftPush( elemI )
              assert boxL == list(range(1, elemI+1))
              assert ret  == None
          
          #single shift pushes
          out      = 1
          for elemI in range(6,9):
              ret  = boxL.shiftPush( elemI )
              assert ret == [out]
              out += 1
          assert boxL == [4,5,6,7,8]
          
          #empty shift push
          ret = boxL.shiftPush()
          assert ret  == None
          assert boxL == [4,5,6,7,8]
          
          #multi shift pushes
          ret = boxL.shiftPush(9,10,11)
          assert ret  == [4,5,6]
          assert boxL == [7,8,9,10,11]
          
          ret = boxL.shiftPush(12,13,14,15,16)
          assert ret  == [7,8,9,10,11]
          assert boxL == [12,13,14,15,16]
          
          ret = boxL.shiftPush(17,18,19,20,21,22,23)
          assert ret  == [12,13,14,15,16,17,18]
          assert boxL == [19,20,21,22,23]          

          print ( "...BoxList.shiftPush tested sucessfully!" )
                              
                    
      #selftest
      @classmethod
      @muteLogging
      def _selftest(self):
          """ 
              Tests whether this class works as expected. It seems to, 
              if no exceptions are raised during the test.
          """
          
          print ( "Testing BoxList..." )          
 
          self._initSelftest()
          self._shiftPushSelftest()
 
          print ( "...BoxList tested successfully!" )
          
          
          
##############################
# Premade Typed List Classes #
##############################
     
#create 'macro'
typedListClassesS = \
"""
class {0}{3}List({2}):
      " A typed '{2}'. Just elements of any type of '{1}' are allowed - other types lead to exceptions. "
      
      #constructor
      @logExceptions
      def __init__(self, *params, **paramDict):
          " All parameters (but 'elemTypesT') just are forwarded to the constructor of parent class '{2}'. "
          
          #ensure, that no tuple of types is given additionally
          if "elemTypesT" in paramDict.keys():
             raise Exception("parameter 'elemTypesT' is not allowed for already (intrinsically) typed lists!")
             
          #call parent's constructor
          extendedParamDict               = paramDict.copy()
          extendedParamDict["elemTypesT"] = tuple({1})
          {2}.__init__(self, *params, **extendedParamDict)
"""

#create list of typed list types to be created
typedListTuplesL = [ ("Int", "[int]"), ("Float", "[float]"), ("Number", "[int, float, Decimal_Decimal]"), \
                     ("Dict", "[dict]"), ("List", "[list]"), ("Tuple", "[tuple]"), ("Str", "[str]"),      \
                     ("Luple", "[list, tuple]"), ("Set", "[set]"), ("Decimal", "[Decimal_Decimal]")       ]

#create typed lists
for looperT in [("EnhList", ""), ("SecList", "Sec")]:
    for typedListT in typedListTuplesL:
        exec( typedListClassesS.format( *(typedListT+looperT) ) )
    
#delete temporary variables
del typedListClassesS
del typedListTuplesL
del looperT
del typedListT

#premade typed list classes selftest
def _premadeTypedListsSelftest():
    """ Selftest for premade typed list classes. """
    
    print ( "Testing premade typed list classes..." )

    tL = IntList(1,3,5)
    assert tL == [1,3,5]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (int,)
    
    tL = FloatList(1.1,3.3,5.5)
    assert tL == [1.1,3.3,5.5]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (float,)
    
    tL = NumberList(1,3.3,Decimal_Decimal(5.5))
    assert tL == [1,3.3,Decimal_Decimal(5.5)]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (int, float, Decimal_Decimal)
    
    tL = DictList({1:11},{3:33},{5:55})
    assert tL == [{1:11},{3:33},{5:55}]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (dict,)
    
    tL = ListList([1],[3],[5])
    assert tL == [[1],[3],[5]]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (list,)
    
    tL = TupleList((1,),(3,),(5,))
    assert tL == [(1,),(3,),(5,)]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (tuple,)
    
    tL = StrList("1","3","5")
    assert tL == ["1","3","5"]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (str,)
    
    tL = LupleList([1],(3,),[5])
    assert tL == [[1],(3,),[5]]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (list,tuple)
    
    tL = SetList(set([1]),set((3,)),set([5]))
    assert tL == [set([1]),set((3,)),set([5])]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (set,)
    
    tL = DecimalList(Decimal_Decimal(1.1), Decimal_Decimal(3.3), Decimal_Decimal(5.5))
    assert tL == [Decimal_Decimal(1.1), Decimal_Decimal(3.3), Decimal_Decimal(5.5)]
    assert isinstance(tL, EnhList)
    assert tL._elemTypesT == (Decimal_Decimal,)
    
    tL = IntSecList(1,3,5)
    assert tL == [1,3,5]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (int,)
    
    tL = FloatSecList(1.1,3.3,5.5)
    assert tL == [1.1,3.3,5.5]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (float,)
    
    tL = NumberSecList(1,3.3,Decimal_Decimal(5.5))
    assert tL == [1,3.3,Decimal_Decimal(5.5)]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (int, float, Decimal_Decimal)
    
    tL = DictSecList({1:11},{3:33},{5:55})
    assert tL == [{1:11},{3:33},{5:55}]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (dict,)
    
    tL = ListSecList([1],[3],[5])
    assert tL == [[1],[3],[5]]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (list,)
    
    tL = TupleSecList((1,),(3,),(5,))
    assert tL == [(1,),(3,),(5,)]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (tuple,)
    
    tL = StrSecList("1","3","5")
    assert tL == ["1","3","5"]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (str,)
    
    tL = LupleSecList([1],(3,),[5])
    assert tL == [[1],(3,),[5]]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (list,tuple)
    
    tL = SetSecList(set([1]),set((3,)),set([5]))
    assert tL == [set([1]),set((3,)),set([5])]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (set,)
    
    tL = DecimalSecList(Decimal_Decimal(1.1), Decimal_Decimal(3.3), Decimal_Decimal(5.5))
    assert tL == [Decimal_Decimal(1.1), Decimal_Decimal(3.3), Decimal_Decimal(5.5)]
    assert isinstance(tL, SecList)
    assert tL._elemTypesT == (Decimal_Decimal,)
    
    print ( "...premade typed list classes tested successfully!" )



##################
### Test Means ###
##################
class TestO(object):
      """ """
      
      def __init__(self, vala, valb=None):
          """ """
          
          self.a = vala   
          self.b = vala if valb == None else valb
          
      def __eq__(self, ohs):
          return (self.a==ohs.a) and (self.b==ohs.b)
 
      def __repr__(self):
          return "(a=%s, b=%s)" % (self.a, self.b)  
          
class TestL(list):
      """ """

      def __init__(self, val):
          """ """
          
          list.__init__(self, (val, val, val))
 
class TestD(dict):
      """ """
      
      def __init__(self, val):
          """ """
          
          dict.__init__(self, a=val, b=val)
          
      def __eq__(self, ohs):
          return (self['a']==ohs['a']) and (self['b']==ohs['b'])
          
 
  
#exec some code not tested in other functions
def _improveCoverage():
    """ 
        Remaining stuff...
        !!!TBD!!! correct error belonging to 'commented block' 
        and check the rest with more detail !!! 
    """
    
    if not isPy3():
       text = STR(unicode("abc"))
       assert isinstance(text, str)
       assert text == "abc"
       
    text = STR("abc")
    assert isinstance(text, str)
    assert text == "abc"
    
    assert getVersion() == 0.9
    
    sL = SecList(1,3,5,7)
#    nL = sL[ (elem > 1) & (lambda el: el < 7) ]
#    assert nL == [3,5]
#    
#    sL = SecList(1,3,5,7)
#    nL = sL[ (elem == 3) | (lambda el: el == 5) ]
#    assert nL == [3,5]
    
    sL.toggleDebugMode(True, "testList")
    sL.push(9)
    sL.pop()
    sL.pop(lambda x: True, single)
    sL.pop(lambda x: True, several)
    sL.toggleDebugMode(False)
    sL.toggleDebugMode()
    sL.toggleDebugMode()
    
    mutex = SemiBlockingMutex()
    mutex.acquire()
    mutex.release()
    with mutex:
         pass


      
#############################
# module selfttest function #
#############################
def selftest():
    """
        Calls all test functions contained in this module.
        If there is no exception resp. assertion error, module seems to do what it
        is expected to.
    """
    
    print ( "Testing Module..." )
    
    _elemSelftest()
    TypedList._selftest()
    EnhList._selftest()
    _improveCoverage()
    
    ### test attribute and item access using 'elem' ###
    #list of objects with attributes 
    print ( "Testing EnhList attribute and item access..." )
    
    enhList = EnhList( range(1,17) )
    poppedL = enhList.pop( ((elem > 3) & (elem < 9)) | ((elem > 9) & (elem < 15)) )
    assert poppedL  == [4,5,6,7,8,10,11,12,13,14]
    assert enhList  == [1,2,3,9,15,16]
    
    #list of objects with attributes 
    enhList = EnhList( map(TestO, range(1,17)) )
    poppedL = enhList.pop( ((elem.a > 3) & (elem.a < 9)) | ((elem.b > 9) & (elem.b < 15)) )
    assert poppedL  == list(map(TestO, [4,5,6,7,8,10,11,12,13,14]))
    assert enhList  == list(map(TestO, [1,2,3,9,15,16]))

    #list of lists 
    enhList = EnhList( map(TestL, range(1,17)) )
    poppedL = enhList.pop( ((elem[0] > 3) & (elem[2] < 9)) | ((elem[0] > 9) & (elem[2] < 15)) )
    assert poppedL  == list(map(TestL, [4,5,6,7,8,10,11,12,13,14]))
    assert enhList  == list(map(TestL, [1,2,3,9,15,16]))  
   
    #list of dictionaries 
    enhList = EnhList( map(TestD, range(1,17)) )
    poppedL = enhList.pop( ((elem['a'] > 3) & (elem['b'] < 9)) | ((elem['a'] > 9) & (elem['b'] < 15)) )
    assert poppedL  == list(map(TestD, [4,5,6,7,8,10,11,12,13,14]))
    assert enhList  == list(map(TestD, [1,2,3,9,15,16]))
    
    print ( "...EnhList attribute and item access tested successfully!" )    
    
    SecList._selftest()    
    BoxList._selftest()
    _premadeTypedListsSelftest()
    
    print ( "...Module tested successfully!" )
    print ( "" )
    print ( "--EVERYTHING SEEMS FINE--" )
    
    
    
__doc__ = \
"""
##############################
# List of Main API Elements: #
##############################

EnhList             : list with enhanced in-place capabilities
SecList             : enhanced list, automatically secured with a lock for multithreading/processing use
BoxList             : under construction

elem                : alias for list element condition / operator functions
single              : alias for single element mode for list methods
several             : alias for several elements mode for list methods

TypeMismatch        : exception raised if the type of a list element is not allowed in a typed list

premade typed lists :
DecimalList           #inherited from EnhList (which inherits from TypedList)
DictList
FloatList
IntList
ListList
LupleList             #elements can be of type list or tuple
NumberList            #elements can be of type int, float and decimal.Decimal
SetList
StrList
TupleList

DecimalSecList        #inherited from SecList (which inherits from EnhList)
DictSecList
FloatSecList
IntSecList
ListSecList
LupleSecList          #elements can be of type list or tuple
NumberSecList         #elements can be of type int, float and decimal.Decimal
SetSecList
StrSecList
TupleSecList


( Further (mostly internal) Elements:
  =================================== 
  
  isPy2()
  isPy3()
  ConditionFunction
  TypedList
  SemiBlockingMutex
  BlockingMutex
  selftest()                          )


############
# EnhList: #
############

""" + EnhList.__doc__ + \
"""


############
# SecList: #
############
""" + SecList.__doc__ + \
"""


############
# BoxList: #
############
""" + BoxList.__doc__      

       
    
    
if __name__ == "__main__":  
   #parse command line arguments
   argParser = Argparse_ArgumentParser()
   argParser.add_argument("--test", action="store_true", help="run code testing this library for errors using test cases.")
   argParser.add_argument("--info", action="store_true", help="print introduction to this library.")
   args      = argParser.parse_args()
   

   #run tests if '--test' is given in command line
   if    args.test == True:          
         selftest()
       
       
   if    args.info == True:
         print (__doc__)
         
         
         
             
#!!!TBD: check BoxList !!!
#!!!TBD: check whether the capabilities of 'elem' should be extended !!!
             


