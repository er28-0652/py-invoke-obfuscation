import random
import string
from pathlib import Path
from functools import singledispatch

from invoke_obfuscation import utils

class ObfuscatorException(Exception):
    pass


class EncodedAsciiCommand:
    '''
    >>> for _ in range(10):
    >>>     EncodedAsciiCommand.invoke('Write-Output AAAAA')
         [String]::Join('' , ( (87 , 114 , 105,116 , 101, 45, 79, 117 , 116 ,112, 117, 116,32 ,65,65,65 ,65 , 65) |%{ ( [CHaR] [INt]$_) } ))|.($ShellId[1]+$ShellId[13]+'x')
        [STRING]::JOIN('', ((87,114,105,116 , 101, 45 ,79,117, 116 ,112,117 ,116 , 32 , 65 ,65 ,65,65 , 65 )|%{([ChaR][INt]$_) }) )| & (([String]$VerbosePreference)[1,3]+'x'-Join'')
         [STRinG]::JOIn( '', ( '87A114K105K116;101r45r79;117t116I112A117A116K32w65A65r65w65A65'.SpLit('w;UI!-rKtA' ) | FOREACH{([CHAR][INt] $_)} ) ) |& (([String]$VerbosePreference)[1,3]+'x'-Join'')
        [STrINg]::JoIN( '',( '87z114G105:116z101%45:79t117t116M112:117u116%32!65_65!65:65:65'.SpLIt('!-G%:Mzu_t')| FOREaCh-ObJEct{([Char][InT] $_)} )) | . ($ShellId[1]+$ShellId[13]+'x')
         & ($ShellId[1]+$ShellId[13]+'x') ( [STriNG]::Join('' , ((87 , 114,105 , 116 ,101, 45,79 ,117 ,116, 112 , 117 , 116 ,32 ,65,65 , 65, 65, 65)|FOrEACh-ObJect{( [Char] [INt]$_)}) )) 
         [STRING]::Join( '' , ( (87, 114, 105 , 116,101 ,45,79 , 117 ,116,112 , 117 , 116,32,65,65 , 65 ,65 , 65) |% { ( [ChaR][InT] $_)} ) )| IEX
         [STriNg]::JOIn( '' , ( (87, 114 ,105 , 116 ,101 ,45 ,79 ,117, 116, 112 , 117, 116, 32 ,65 , 65 , 65,65, 65 )|ForEaCH { ( [CHaR][INt] $_)}))| .($ShellId[1]+$ShellId[13]+'x')
        INvokE-EXPrESSiON ( [STRInG]::JoIn( '',((87, 114 ,105 , 116,101 , 45 ,79 ,117 , 116,112,117,116 ,32,65,65 , 65 , 65 ,65)| %{ ([CHar][INt] $_) }) )) 
         . ($ShellId[1]+$ShellId[13]+'x') ( [StrInG]::JOin('' , [CHaR[]] (87,114, 105 ,116,101 ,45 , 79 , 117, 116 ,112 ,117,116 ,32 ,65 ,65 ,65 ,65 , 65 )))
        .($ShellId[1]+$ShellId[13]+'x')( [StRiNg]::JOin('', ('87s114u105!116y101!45v79;117!116i112T117i116}32u65T65~65y65~65'.SPLit( 'i}vy~T!;us' )|% {([CHAR] [INt] $_)} ) ))
    '''

    def __init__(self, code):
        self.code = code

        self.delimiters = list('_-,{}~!@%&<>;:')
        self.random_delimiters = []
    
    def _init_delimiters(self):
        chars = [c.upper() if utils.is_good_luck() else c for c in string.ascii_lowercase]
        self.random_delimiters = random.sample(chars+self.delimiters, len(chars+self.delimiters)//4)
    
    @property
    def random_delimiters_to_print(self):
        return "".join([s for s in self.random_delimiters])
    
    @property
    def delimited_encoded_array(self):
        return "".join([str(ord(c)) + random.choice(self.random_delimiters) for c in self.code])[:-1]
    
    @property
    def encoded_array(self):
        return "({})".format(
            "".join(["{0}{1},{2}".format(ord(c), utils.make_random_space(), utils.make_random_space()) for c in self.code]).rstrip()[:-1])
    
    @property
    def random_conversion_syntax(self):
        return "[{}]{}[{}]{}$_".format(
            self.char_str, utils.make_random_space(), self.int_str, utils.make_random_space())
    
    @property
    def str_join(self):
        return utils.make_str_to_lower_or_upper('[String]::Join')
    
    @property
    def str_str(self):
        return utils.make_str_to_lower_or_upper('[String]')
    
    @property
    def char_str(self):
        return utils.make_str_to_lower_or_upper('Char')
    
    @property
    def int_str(self):
        return utils.make_str_to_lower_or_upper('Int')
    
    @property
    def for_each_object(self):
        return utils.make_str_to_lower_or_upper(random.choice(['ForEach','ForEach-Object','%']))
    
    def _make_invoke_expression_ptn1(self):
        return utils.make_str_to_lower_or_upper(random.choice(['IEX','Invoke-Expression']))
    
    def _make_invoke_expression_ptn2(self):
        return "{0}{1}({2}+'x')".format(
            random.choice(['.','&']), #0
            utils.make_random_space(), #1
            "$ShellId[1]+$ShellId[13]" #2
        )

    def _make_invoke_expression_ptn3(self):
        return "{0}{1}({2}[1,3]+'x'-Join'')".format(
            random.choice(['.','&']), #0
            utils.make_random_space(), #1
            random.choice(['$VerbosePreference.ToString()','([String]$VerbosePreference)']), #2
        )

    def invoke_expression(self, invoke_exp_ptn=None):
        if invoke_exp_ptn == 1:
            return self._make_invoke_expression_ptn1()
        elif invoke_exp_ptn == 2:
            return self._make_invoke_expression_ptn2()
        elif invoke_exp_ptn == 3:
            return self._make_invoke_expression_ptn3()
        else:
            return random.choice(
                [self._make_invoke_expression_ptn1, self._make_invoke_expression_ptn2, self._make_invoke_expression_ptn3])()
        
    def _make_base_script_ptn1(self):
        return "({0}'{1}'.{2}({3}'{4}'{5}){6}|{7}{8}{9}{{{10}({11}{12}){13}}}{14})".format(
            utils.make_random_space(),
            self.delimited_encoded_array,
            utils.make_str_to_lower_or_upper('Split'),
            utils.make_random_space(),
            self.random_delimiters_to_print,
            utils.make_random_space(), #5
            utils.make_random_space(),
            utils.make_random_space(),
            self.for_each_object, #8
            utils.make_random_space(), #9
            utils.make_random_space(), #10
            utils.make_random_space(), #11
            self.random_conversion_syntax, #12
            utils.make_random_space(), #13
            utils.make_random_space() #14
        )
    
    def _make_base_script_ptn2(self):
        return "[{0}[]]{1}{2}".format(self.char_str, utils.make_random_space(), self.encoded_array)
    
    def _make_base_script_ptn3(self):
        return "({0}{1}{2}|{3}{4}{5}{{{6}({7}{8}){9}}}{10})".format(
            utils.make_random_space(), #0
            self.encoded_array, #1
            utils.make_random_space(), #2
            utils.make_random_space(), #3
            self.for_each_object, #4
            utils.make_random_space(), #5
            utils.make_random_space(), #6
            utils.make_random_space(), #7
            self.random_conversion_syntax, #8
            utils.make_random_space(), #9
            utils.make_random_space() #10
        )
    
    def base_script(self, base_script_ptn=None):
        if base_script_ptn == 1:
            return self._make_base_script_ptn1()
        elif base_script_ptn == 2:
            return self._make_base_script_ptn2()
        elif base_script_ptn == 3:
            return self._make_base_script_ptn3()
        elif base_script_ptn is None or self.raise_exception is False:
            return random.choice(
                [self._make_base_script_ptn1, self._make_base_script_ptn2, self._make_base_script_ptn3])()
        else:
            raise ObfuscatorException('wrong option for base_script, given ptn is {}'.format(base_script_ptn))
    
    def new_script(self, base_script_ptn=None):
        return "{0}({1}''{2},{3}{4}{5})".format(
            self.str_join, #0
            utils.make_random_space(), #1
            utils.make_random_space(), #2
            utils.make_random_space(), #3
            self.base_script(base_script_ptn), #4
            utils.make_random_space() #5
        )

    def _make_invoke_option_ptn1(self, base_script_ptn=None, invoke_expression_ptn=None):
        return "{0}{1}{2}({3}{4}{5}){6}".format(
            utils.make_random_space(), #0
            self.invoke_expression(invoke_expression_ptn), #1
            utils.make_random_space(), #2
            utils.make_random_space(), #3
            self.new_script(base_script_ptn), #4
            utils.make_random_space(), #5
            utils.make_random_space(), #6
        )

    def _make_invoke_option_ptn2(self, base_script_ptn=None, invoke_expression_ptn=None):
        return "{0}{1}{2}|{3}{4}".format(
            utils.make_random_space(), #0
            self.new_script(base_script_ptn), #1
            utils.make_random_space(), #2
            utils.make_random_space(), #3
            self.invoke_expression(invoke_expression_ptn) #4
        )
    
    def invoke_option(self, base_script_ptn=None, invoke_expression_ptn=None, invoke_ptn=None):
        if invoke_ptn == 1:
            return self._make_invoke_option_ptn1(base_script_ptn, invoke_expression_ptn)
        elif invoke_ptn == 2:
            return self._make_invoke_option_ptn2(base_script_ptn, invoke_expression_ptn)
        else:
            return self._make_invoke_option_ptn1(base_script_ptn, invoke_expression_ptn) if utils.is_good_luck() else self._make_invoke_option_ptn2(base_script_ptn, invoke_expression_ptn)

    def _invoke(self, base_script_ptn=None, invoke_expression_ptn=None, invoke_ptn=None):
        self._init_delimiters()
        return self.invoke_option(base_script_ptn, invoke_expression_ptn, invoke_ptn)

    @singledispatch
    @staticmethod
    def invoke(arg, base_script_ptn=None, invoke_expression_ptn=None, invoke_ptn=None):
        pass
    
    @invoke.register(str)
    def _(arg, base_script_ptn=None, invoke_expression_ptn=None, invoke_ptn=None):
        eac = EncodedAsciiCommand(arg)
        return eac._invoke(invoke_expression_ptn, invoke_ptn)
    
    @invoke.register(Path)
    def _(arg, base_script_ptn=None, invoke_expression_ptn=None, invoke_ptn=None):
        if not arg.exists():
            raise RuntimeError(f'{arg} does not exist.')
        eac = EncodedAsciiCommand(arg.read_text())
        return eac._invoke(invoke_expression_ptn, invoke_ptn)