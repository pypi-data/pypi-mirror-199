from typing import overload, Any, Callable, Union, NoReturn, Optional, Tuple, Type

_Iterable = Union[list,dict]
_Key = Union[int,Any]
_Value = Any
_Temp = _Value
_Next = _Value
_Desc = bool


class EnumerableBase:
    def __init__(self, iterable:_Iterable):
        self.iterable = iterable
    
    def Get(self, *key:_Key) -> _Value:
        iterable = self.iterable
        for k in key:
            if (k < len(iterable) if EnumerableBase(iterable).IsType(list) else k in EnumerableBase(iterable).GetKeys()):
                iterable = iterable[k]
            else:
                raise IndexError()
        return iterable
    def GetKey(self, value:_Value) -> _Key:
        if self.IsType(dict):
            return list(self.GetKeys())[list(self.GetValues()).index(value)]
        else:
            return self.iterable.index(value)
    def GetKeys(self, *key:_Key) -> list:
        iterable = self.Get(*key)
        if EnumerableBase(iterable).IsType(dict):
            return list(iterable.keys())
        else:
            return list(range(len(iterable)))
    def GetValues(self, *key:_Key) -> list:
        iterable = self.Get(*key)
        if EnumerableBase(iterable).IsType(dict):
            return list(iterable.values())
        else:
            return iterable
    def GetItems(self, *key:_Key) -> list:
        iterable = self.Get(*key)
        if EnumerableBase(iterable).IsType(dict):
            return list(iterable.items())
        else:
            return list(enumerate(iterable))
    
    def Take(self, count:int) -> _Iterable:
        if self.IsType(dict): 
            return dict(self.GetItems()[:count])
        else:
            return self.iterable[:count]
    def TakeLast(self, count:int) -> _Iterable:
        return self.Skip(self.Lenght()-count)
    def Skip(self, count:int) -> _Iterable:
        if self.IsType(dict): 
            return dict(self.GetItems()[count:])
        else:
            return self.iterable[count:]
    def SkipLast(self, count:int) -> _Iterable:
        return self.Take(self.Lenght()-count)
    @overload
    def Select(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> _Iterable: ...
    @overload
    def Select(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value, key_func:Callable[[_Key,_Value],_Value]=lambda key, value: key) -> _Iterable: ...
    def Select(self, f1=lambda k,v: v, f2=...) -> _Iterable:
        if self.IsType(dict):
            return dict(zip((self.GetKeys() if f2 is ... else map(f2,self.GetKeys(),self.GetValues())),map(f1,self.GetKeys(),self.GetValues())))
        else:
            return list(map(f1,range(self.Lenght()),self.iterable))
    def Distinct(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> _Iterable:
        new_iterable = self.Copy()
        index = 0
        for key, value in self.GetItems():
            if EnumerableBase(new_iterable).Count(func(key, value), func) > 1:
                if self.IsType(list):
                    key -= index
                EnumerableBase(new_iterable).Delete(key)
                index += 1
        return new_iterable
    def Except(self, *value:_Value, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> _Iterable:
        new_iterable = self.Copy()
        for k, v in self.GetItems():
            if func(k,v) in value:
                EnumerableBase(new_iterable).Remove(v)
        return new_iterable
    def Where(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True, getkey:bool=False) -> _Iterable:
        result = dict()
        for key, value in EnumerableBase(self.ToDict()).GetItems():
            if func(key, value):
                result[key] = value
        if not getkey:
            result = list(result.values())
        return result
    def OfType(self, *type:Type, getkey:bool=False) -> _Iterable:
        return self.Where(lambda key,value: isinstance(value,type), getkey)
    def First(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Tuple[_Key,_Value]]:
        iterable = EnumerableBase(self.ToDict()).GetItems()
        for key, value in iterable:
            if func(key, value):
                return (key,value)
        return None
    def Last(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Tuple[_Key,_Value]]:
        result = self.Where(func, getkey=True)
        if len(result) == 0:
            return None
        else:
            return list(result.items())[-1]
    def Single(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Tuple[_Key,_Value]]:
        result = self.Where(func, getkey=True)
        if len(result) != 1:
            return None
        else:
            return list(result.items())[0]
    def Join(self, iterable:_Iterable, inner:Callable[[_Key,_Value],bool]=lambda key, value: value, outer:Callable[[_Key,_Value],bool]=lambda key, value: value, func:Callable[[_Key,_Value,_Key,_Value],bool]=lambda inner, outher: (inner, outher))  -> list:
        new_iterable = []
        for outKey, outValue in EnumerableBase(iterable).GetItems():
            new_iterable.append((self.First(lambda inKey, inValue: outer(outKey, outValue) == inner(inKey, inValue))[1], outValue))
        return EnumerableBase(new_iterable).Select(lambda key, value: func(value[0], value[1]))           
    def OrderBy(self, *func:Callable[[[_Key,_Value],_Value],_Desc]) -> _Iterable:
        if func == ():
            func = (lambda key, value: value)
        iterable = self.GetItems()
        func:list = list(func)
        func.reverse()
        for f, desc in func:
            iterable = sorted(iterable, key=lambda x: f(x[0],x[1]), reverse=desc)
        if EnumerableBase(iterable).IsType(dict):
            return dict(iterable)
        else:
            return list(dict(iterable).values())
    def Reverse(self) -> _Iterable:
        if self.IsType(dict):
            return dict(EnumerableBase(self.GetKeys().reverse()).Zip(self.GetValues().reverse()))
        else:
            return list(reversed(self.iterable))
    def Zip(self, iterable:_Iterable, func:Callable[[_Key,_Value,_Key,_Value],_Value]=lambda key, value, newKey, newValue: (value, newValue)) -> list:
        return EnumerableBase(list(zip(self.GetItems(),EnumerableBase(iterable).GetItems()))).Select(lambda index, value: func(value[0][0],value[0][1],value[1][0],value[1][1]))

    def Any(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> bool:
        result = False
        iterable = EnumerableBase(self.ToDict()).GetItems()
        for key, value in iterable:
            if func(key, value):
                result = True
                break
        return result
    def All(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> bool:
        result = True
        iterable = EnumerableBase(self.ToDict()).GetItems()
        for key, value in iterable:
            if not func(key, value):
                result = False
                break
        return result
    def SequenceEqual(self, iterable:_Iterable) -> bool:
        result =  EnumerableBase(EnumerableBase(self.iterable).Zip(iterable, lambda key, value, newKey, newValue: (key, value, newKey, newValue)))
        if self.IsType(dict):
            return result.All(lambda index, value: value[0] is value[2] and value[1] is value[3])
        else:
            return result.All(lambda index, value: value[0] == value[2] and value[1] is value[3])

    def Aggregate(self, func:Callable[[_Temp,_Key,_Next],bool]=lambda _temp, key, value: _temp + value, result_func:Callable[[_Key,_Value],bool]=lambda key, value: value) -> _Temp:
        result = None
        for key, value in self.GetItems():
            if result is None:
                result = result_func(key, value)
            else:
                result = func(result, key, value)
        return result  

    def Count(self, value:_Value, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> int:
        iterable = self.Select(func)
        if EnumerableBase(iterable).IsType(dict):
            return list(iterable.values()).count(value)
        else:
            return iterable.count(value)
    def Lenght(self) -> int:
        return len(self.iterable)
    def Sum(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Optional[int]:
        iterable = self.Select(func)
        if EnumerableBase(iterable).OfType(int,float):
            iterable = EnumerableBase(iterable).GetValues()
            return sum(iterable)
        else:
            return None
    def Avg(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Optional[int]:
        iterable = self.Select(func)
        if EnumerableBase(iterable).OfType(int,float):
            iterable = EnumerableBase(iterable).GetValues()
            return sum(iterable) / self.Lenght()
        else:
            return None
    def Max(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Optional[int]:
        iterable = self.Select(func)
        if EnumerableBase(iterable).OfType(int,float):
            iterable = EnumerableBase(iterable).GetValues()
            return max(iterable)
        else:
            return None
    def Min(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Optional[int]:
        iterable = self.Select(func)
        if EnumerableBase(iterable).OfType(int,float):
            iterable = EnumerableBase(iterable).GetValues()
            return min(iterable)
        else:
            return None

    @overload
    def Add(self, value:_Value): ...
    @overload
    def Add(self, key:_Key, value:_Value): ...
    def Add(self, v1, v2=...):
        if self.IsType(dict):
            self.iterable[v1] = v2
        else:
            self.iterable.append(v1)
    @overload
    def Prepend(self, value:_Value): ...
    @overload
    def Prepend(self, key:_Key, value:_Value): ...
    def Prepend(self, v1, v2=...):
        if self.IsType(dict):
            new_iterable = {v1: v2}
            new_iterable.update(self.iterable)
        else:
            new_iterable = [v1]
        self.Clear()
        self.Concat(new_iterable)
    def Insert(self, key:_Key, value:_Value):
        if self.IsType(dict):
            self.iterable[key] = value
        else:
            self.iterable.insert(key, value)
    def Update(self, key:_Key, value:_Value):
        self.iterable[key] = value
    def Concat(self, *iterable):
        for i in iterable:
            if self.IsType(dict):
                self.iterable.update(i)
            else:
                self.iterable.extend(i)
    def Delete(self, *key:_Key):
        for k in key:
            self.iterable.pop(k)
    def Remove(self, *value:_Value, all:bool=False):
        for v in value:
            if self.IsType(dict):
                self.iterable.pop(self.First(lambda k, va: va == v)[0])
            else:
                if all:
                    while True:
                        if self.Count(v) == 0:
                            break
                        self.iterable.remove(v)
                else:
                    self.iterable.remove(v)
    def Clear(self):
        self.iterable.clear()
    @overload
    def Map(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> _Iterable: ...
    @overload
    def Map(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value, key_func:Callable[[_Key,_Value],_Value]=lambda key, value: key) -> _Iterable: ...
    def Map(self, f1=lambda k,v: v, f2=...):
        new_iterable = self.Select( f1, f2)
        self.Clear()
        self.Concat(new_iterable)

    def Loop(self, func:Callable[[_Iterable, _Iterable, _Key,_Value],NoReturn]=lambda iterable, result, key, value: print(key,value), iterable:Optional[_Iterable]=None, result:list=[]) -> list:
        if iterable is None:
            iterable = self.iterable
        for key, value in self.GetItems():
            func(iterable, result, key, value)    
        return result

    def Copy(self) -> _Iterable:
        return self.iterable.copy()

    def ToList(self) -> list:
        return (self.Copy() if self.IsType(list) else list(self.iterable.values()))
    def ToDict(self) -> dict:
        return (self.Copy() if self.IsType(dict) else dict(enumerate(self.iterable)))

    def IsEmpty(self) -> bool:
        return self.iterable in [[],{},None]
    def IsType(self, *type:Type):
        return isinstance(self.iterable,type)

__all__ = [
    "_Key", "_Value", "_Temp", "_Next", "_Iterable", "EnumerableBase"
]
