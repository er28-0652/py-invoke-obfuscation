import random
import string

def is_good_luck():
    return 0.5 > random.random()

def make_str_to_lower_or_upper(text):
    return "".join([c.upper() if is_good_luck() else c for c in text])

def make_random_space():
    return " "*random.choice([0, 1])


class PSObfuscator:
    """
    >>> import io
    >>> obf = PSObfuscator(io.StringIO("Write-Output AAAAA"))
    >>> for _ in range(10):
    >>>     obf.invoke()
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
    """

    def __init__(self, code):
        assert hasattr(code, "read")
        self.code = code.read()
        
        self.delimiters = ['_','-',',','{','}','~','!','@','%','&','<','>',';',':']
        self.random_delimiters = None
    
    def _init_delimiters(self):
        chars = [c.upper() if is_good_luck() else c for c in string.ascii_lowercase]
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
            "".join(["{0}{1},{2}".format(ord(c), make_random_space(), make_random_space()) for c in self.code]).rstrip()[:-1])
    
    @property
    def random_conversion_syntax(self):
        return "[{}]{}[{}]{}$_".format(
            self.char_str, make_random_space(), self.int_str, make_random_space())
    
    @property
    def str_join(self):
        return make_str_to_lower_or_upper('[String]::Join')
    
    @property
    def str_str(self):
        return make_str_to_lower_or_upper('[String]')
    
    @property
    def char_str(self):
        return make_str_to_lower_or_upper('Char')
    
    @property
    def int_str(self):
        return make_str_to_lower_or_upper('Int')
    
    @property
    def for_each_object(self):
        return make_str_to_lower_or_upper(random.choice(['ForEach','ForEach-Object','%']))
    
    def _make_invoke_expression_ptn1(self):
        return make_str_to_lower_or_upper(random.choice(['IEX','Invoke-Expression']))
    
    def _make_invoke_expression_ptn2(self):
        return "{0}{1}({2}+'x')".format(
            random.choice(['.','&']), #0
            make_random_space(), #1
            "$ShellId[1]+$ShellId[13]" #2
        )

    def _make_invoke_expression_ptn3(self):
        return "{0}{1}({2}[1,3]+'x'-Join'')".format(
            random.choice(['.','&']), #0
            make_random_space(), #1
            random.choice(['$VerbosePreference.ToString()','([String]$VerbosePreference)']), #2
        )

    @property
    def invoke_expression(self):
        return random.choice(
            [self._make_invoke_expression_ptn1, self._make_invoke_expression_ptn2, self._make_invoke_expression_ptn3])()
    
    def _make_base_script_ptn1(self):
        return "({0}'{1}'.{2}({3}'{4}'{5}){6}|{7}{8}{9}{{{10}({11}{12}){13}}}{14})".format(
            make_random_space(),
            self.delimited_encoded_array,
            make_str_to_lower_or_upper('Split'),
            make_random_space(),
            self.random_delimiters_to_print,
            make_random_space(), #5
            make_random_space(),
            make_random_space(),
            self.for_each_object, #8
            make_random_space(), #9
            make_random_space(), #10
            make_random_space(), #11
            self.random_conversion_syntax, #12
            make_random_space(), #13
            make_random_space() #14
        )
    
    def _make_base_script_ptn2(self):
        return "[{0}[]]{1}{2}".format(self.char_str, make_random_space(), self.encoded_array)
    
    def _make_base_script_ptn3(self):
        return "({0}{1}{2}|{3}{4}{5}{{{6}({7}{8}){9}}}{10})".format(
            make_random_space(), #0
            self.encoded_array, #1
            make_random_space(), #2
            make_random_space(), #3
            self.for_each_object, #4
            make_random_space(), #5
            make_random_space(), #6
            make_random_space(), #7
            self.random_conversion_syntax, #8
            make_random_space(), #9
            make_random_space() #10
        )
    
    @property
    def base_script(self):
        return random.choice([self._make_base_script_ptn1, self._make_base_script_ptn2, self._make_base_script_ptn3])()
    
    @property
    def new_script(self):
        return "{0}({1}''{2},{3}{4}{5})".format(
            self.str_join, #0
            make_random_space(), #1
            make_random_space(), #2
            make_random_space(), #3
            self.base_script, #4
            make_random_space() #5
        )

    def _make_invoke_option_ptn1(self):
        return "{0}{1}{2}({3}{4}{5}){6}".format(
            make_random_space(), #0
            self.invoke_expression, #1
            make_random_space(), #2
            make_random_space(), #3
            self.new_script, #4
            make_random_space(), #5
            make_random_space(), #6
        )

    def _make_invoke_option_ptn2(self):
        return "{0}{1}{2}|{3}{4}".format(
            make_random_space(), #0
            self.new_script, #1
            make_random_space(), #2
            make_random_space(), #3
            self.invoke_expression #4
        )
    
    @property
    def invoke_option(self):
        return self._make_invoke_option_ptn1() if is_good_luck() else self._make_invoke_option_ptn2()
    
    def invoke(self):
        self._init_delimiters()
        return self.invoke_option

def make_obf(filepath):
    with open(filepath, "r") as f:
        return PSObfuscator(f).invoke()
