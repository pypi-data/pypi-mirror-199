from typing import Callable, NoReturn, Optional, Tuple, Union, Type, overload
from linqex.builds import *
_ListOrDict = Optional[Type[Union[list,dict]]]

version = '1.3'

def enumerable_catch(linq:"Enumerable",iterable:_Iterable, items:bool=False, onevalue:bool=False, iskey:bool=True) -> Optional[Union["Enumerable",_Iterable]]:
    if items:
        if iterable is None:
            return None
        else:
            new_enumerable = Enumerable(iterable[1] if isinstance(iterable[1], (dict,list)) and not onevalue else [iterable[1]])
            if iskey:
                new_enumerable._keyshistory = linq._keyshistory.copy()
                if isinstance(iterable[0],tuple):
                    new_enumerable._keyshistory.extend(iterable[0])
                else:
                    new_enumerable._keyshistory.append(iterable[0])
    else:
        new_enumerable = Enumerable(iterable)
        if iskey:
            new_enumerable._keyshistory = linq._keyshistory.copy()
    new_enumerable.consttype = linq.consttype
    new_enumerable._onevalue = onevalue
    new_enumerable._main = linq._main
    new_enumerable._orderby = linq._orderby
    return new_enumerable
def enumerable_to_value(enumerable_or_value:Union["Enumerable",_Value]):
    if isinstance(enumerable_or_value, Enumerable):
        return enumerable_or_value.ToValue
    else:
        return enumerable_or_value

class Enumerable():
    def __init__(self, iterable:_Iterable, consttype:_ListOrDict=None):
        self.iterable = enumerable_to_value(iterable)
        self.consttype = consttype
        self._keyshistory = list()
        self._main:Enumerable = self
        self._onevalue = False
        self._orderby = list()
        if self.consttype is None:
            self.consttype = (list,dict)
        if not self.IsType(self.consttype):
            if self.IsType(tuple,set):
                self.iterable = list(self.iterable)
            else:
                raise TypeError("'{}' object is not iterable".format(str(type(self.iterable))))
    def __call__(self, iterable:_Iterable):
        self.__init__(iterable)

    def Get(self, *key:_Key) -> Union["Enumerable",_Value]:
        result = EnumerableBase(self.iterable).Get(*key)
        if isinstance(result,(list,dict)):
            return enumerable_catch(self,(key,result),items=True)
        else:
            return result
    def GetKey(self, value:_Value) -> _Key:
        value = enumerable_to_value(value)
        return EnumerableBase(self.iterable).GetKey(value)
    def GetValues(self, *key:_Key) -> list:
        return EnumerableBase(self.iterable).GetValues(*key)
    def GetKeys(self, *key:_Key) -> list:
        return EnumerableBase(self.iterable).GetKeys(*key)
    def GetItems(self,*key:_Key) -> list:
        return EnumerableBase(self.iterable).GetItems(*key)
    
    def Take(self, count:int) -> "Enumerable":
        return enumerable_catch(self,EnumerableBase(self.iterable).Take(count), iskey=False)
    def TakeLast(self, count:int) -> "Enumerable":
        return enumerable_catch(self,EnumerableBase(self.iterable).TakeLast(count), iskey=False)
    def Skip(self, count:int) -> "Enumerable":
        return enumerable_catch(self,EnumerableBase(self.iterable).Skip(count), iskey=False)
    def SkipLast(self, count:int) -> "Enumerable":
        return enumerable_catch(self,EnumerableBase(self.iterable).SkipLast(count), iskey=False)

    @overload
    def Select(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> "Enumerable": ...
    @overload
    def Select(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value, key_func:Callable[[_Key,_Value],_Value]=lambda key, value: key) -> "Enumerable": ...
    def Select(self, f1=lambda k,v: v, f2=...) -> "Enumerable":
        return enumerable_catch(self,EnumerableBase(self.iterable).Select(f1, f2), iskey=False)
    def Distinct(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> "Enumerable":
        return enumerable_catch(self,EnumerableBase(self.iterable).Distinct(func), iskey=False)
    def Except(self, *value:_Value, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> "Enumerable":
        return enumerable_catch(self,EnumerableBase(self.iterable).Except(*list(map(lambda value: enumerable_to_value(value), list(value))), func=func), iskey=False)
    def Where(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True, getkey:bool=False) -> "Enumerable":
        return enumerable_catch(self,EnumerableBase(self.iterable).Where(func, getkey), iskey=False)
    def OfType(self, *types:Type, getkey:bool=False) -> "Enumerable":
        return enumerable_catch(self,EnumerableBase(self.iterable).OfType(*types, getkey=getkey))
    def First(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Union["Enumerable",_Value]]:
        return enumerable_catch(self,EnumerableBase(self.iterable).First(func),items=True,onevalue=True)
    def Last(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Union["Enumerable",_Value]]:
        return enumerable_catch(self,EnumerableBase(self.iterable).Last(func),items=True,onevalue=True)
    def Single(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Union["Enumerable",_Value]]:
        return enumerable_catch(self,EnumerableBase(self.iterable).Single(func),items=True,onevalue=True)    
    def Join(self, iterable:_Iterable, inner:Callable[[_Key,_Value],bool]=lambda key, value: value, outer:Callable[[_Key,_Value],bool]=lambda key, value: value, func:Callable[[_Key,_Value,_Key,_Value],bool]=lambda inner, outher: (inner, outher)) -> "Enumerable":
        return Enumerable(EnumerableBase(self.iterable).Join(enumerable_to_value(iterable), inner, outer, func))
    def OrderBy(self, func:Callable[[_Key,_Value],bool]=lambda key, value: value, desc:bool=False) -> "Enumerable":
        self._orderby.clear()
        self._orderby.append((func, desc))
        enumerable = enumerable_catch(self,EnumerableBase(self.iterable).OrderBy(*self._orderby), iskey=False)
        return enumerable
    def ThenBy(self, func:Callable[[_Key,_Value],_Value], desc:bool=False) -> "Enumerable":
        self._orderby.append((func, desc))
        enumerable = enumerable_catch(self,EnumerableBase(self.iterable).OrderBy(*self._orderby), iskey=False)
        return enumerable
    def Reverse(self) -> _Iterable:
        return enumerable_catch(self, EnumerableBase(self.iterable).Reverse(), iskey=False)
    def Zip(self, iterable:_Iterable, func:Callable[[_Key,_Value,_Key,_Value],_Value]=lambda key, value, newKey, newValue: (value, newValue)) -> list:
        return Enumerable(EnumerableBase(self.iterable).Zip(enumerable_to_value(iterable), func))

    def Any(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> bool:
        return EnumerableBase(self.iterable).Any(func)
    def All(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> bool:
        return EnumerableBase(self.iterable).All(func)
    def SequenceEqual(self, iterable:_Iterable) -> bool:
        return EnumerableBase(self.iterable).SequenceEqual(enumerable_to_value(iterable))

    def Aggregate(self, func:Callable[[_Temp,_Key,_Value],bool]=lambda result, key, nextValue: result + nextValue, result_func:Callable[[_Key,_Value],bool]=lambda key, value: value) -> _Temp:
        return EnumerableBase(self.iterable).Aggregate(func, result_func)

    def Count(self, value:_Value, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> int:
        return EnumerableBase(self.iterable).Count(enumerable_to_value(value), func)
    @property
    def Lenght(self) ->  int:
        return EnumerableBase(self.iterable).Lenght()
    def Sum(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Optional[int]:
        return EnumerableBase(self.iterable).Sum(func)
    def Avg(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Optional[int]:
        return EnumerableBase(self.iterable).Avg(func)
    def Max(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Optional[int]:
        return EnumerableBase(self.iterable).Max(func)
    def Min(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Optional[int]:
        return EnumerableBase(self.iterable).Min(func)
    
    def Set(self, value:_Value):
        value = enumerable_to_value(value)
        if len(self._keyshistory) == 0:
            self.iterable = value
        else:
            self._main.Get(*self._keyshistory[:len(self._keyshistory)-1]).Update(self.ToKey, value)
            self.iterable = value
    @overload
    def Add(self, value:_Value): ...
    @overload
    def Add(self, key:_Key, value:_Value): ...
    def Add(self, v1, v2=...):
        v1, v2 = enumerable_to_value(v1), enumerable_to_value(v2)
        EnumerableBase(self.iterable).Add(v1,v2)
    @overload
    def Prepend(self, value:_Value): ...
    @overload
    def Prepend(self, key:_Key, value:_Value): ...
    def Prepend(self, v1, v2=...):
        v1, v2 = enumerable_to_value(v1), enumerable_to_value(v2)
        EnumerableBase(self.iterable).Prepend(v1,v2)
    def Insert(self, key:_Key, value:_Value):
        key, value = enumerable_to_value(key), enumerable_to_value(value)
        EnumerableBase(self.iterable).Insert(key, value)
    def Update(self, key:_Key, value:_Value):
        value = enumerable_to_value(value)
        EnumerableBase(self.iterable).Update(key, value)
    def Concat(self, *iterable:_Iterable):
        EnumerableBase(self.iterable).Concat(*list(map(lambda v: enumerable_to_value(v), list(iterable))))
    @overload
    def Delete(self): ...
    @overload
    def Delete(self, *key:_Key): ...
    def Delete(self, *v1):
        if v1 == ():
            self._main.Get(*self._keyshistory[:len(self._keyshistory)-1]).Delete(self.ToKey)
        else:
            EnumerableBase(self.iterable).Delete(*v1)
    def Remove(self, *value:_Value, all:bool=False):
        EnumerableBase(self.iterable).Remove(*list(map(lambda v: enumerable_to_value(v), list(value))), all=all)
    def Clear(self):
        EnumerableBase(self.iterable).Clear()
    @overload
    def Map(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value): ...
    @overload
    def Map(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value, key_func:Callable[[_Key,_Value],_Value]=lambda key, value: key): ...
    def Map(self, f1=lambda k,v: v, f2=...):
        EnumerableBase(self.iterable).Map(f1, f2)

    def Loop(self, func:Callable[["Enumerable","Enumerable",_Key,NoReturn],_Value]=lambda self, result, key, value: print(key,value)) -> "Enumerable":
        return Enumerable(EnumerableBase(self.iterable).Loop(func, iterable=self, result=Enumerable.List()))
    def Copy(self) -> "Enumerable":
        return Enumerable(EnumerableBase(self.iterable).Copy())
    
    def IsType(self, *type:Type) -> bool:
        return EnumerableBase(self.iterable).IsType(*type)
    @property
    def IsEmpty(self) -> bool:
        return EnumerableBase(self.iterable).IsEmpty()
    
    def IsKey(self, key:_Key) -> bool:
        if key == self.ToKey:
            return True
        else:
            return False
    def IsValue(self, value:_Value) -> bool:
        value = enumerable_to_value(value)
        if value == self.ToValue:
            return True
        else:
            return False
    def ContainsByKey(self, *key:_Key) -> bool:
        iterable = self.GetKeys()
        for k in key:
            if not k in iterable:
                return False
        return True
    def Contains(self, *value:_Value) -> bool:
        iterable = self.GetValues()
        for v in list(map(lambda v: enumerable_to_value(v), list(value))):
            if not v in iterable:
                return False
        return True

    def ConvertToList(self, const:bool=False) -> "Enumerable":
        if self.IsType(dict):
            self.Set(self.ToList)
            if const:
                self.consttype = dict
        return self
    def ConvertToDict(self, const:bool=False) -> "Enumerable":
        if self.IsType(list):
            self.Set(self.ToDict)
            if const:
                self.consttype = list
        return self
    
    @property
    def ToKey(self) -> _Key:
        if self._keyshistory == []:
            return None
        else:
            return self._keyshistory[-1]
    @property
    def ToValue(self) -> _Value:
        if len(self.iterable) == 1 and self._onevalue:
            return self.GetValues()[0]
        else:
            if self.IsType(list,dict):
                return self.iterable.copy()
            else:
                return self.iterable
    @property
    def ToList(self) -> _Iterable:
        return EnumerableBase(self.iterable).ToList()
    @property
    def ToDict(self) -> _Iterable:
        return EnumerableBase(self.iterable).ToDict()
    
    @staticmethod
    def List(const:bool=False) -> "Enumerable":
        return Enumerable(list(), consttype=list if const else None)
    @staticmethod
    def Dict(const:bool=False) -> "Enumerable":
        return Enumerable(dict(), consttype=dict if const else None)
    @staticmethod
    def Range(start:int, stop:int, step:int=1, const:bool=False) -> "Enumerable":
        return Enumerable(list(range(start,stop,step)), consttype=list if const else None) 
    @staticmethod
    def Repeat(value:_Value, count:int, const:bool=False):
        return Enumerable([enumerable_to_value(value)] * count, consttype=list if const else None)

    def __len__(self):
        return self.Lenght
    def __bool__(self):
        return not self.IsEmpty
    def __getitem__(self,key):
        return self.Get(key)
    def __setitem__(self,key,value):
        self.Update(key,value)
    def __delitem__(self,key):
        self.Delete(key)


__all__ = [
    "Enumerable", "version"
]
