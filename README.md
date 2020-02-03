# py-invoke-obfuscation

Python implementation of Invoke-Obfuscation for PowerShell.  
Not fully implemented though ;)

## Usage
```python
from invoke_obfuscation.encoded_ascii_command import EncodedAsciiCommand

EncodedAsciiCommand.invoke('Write-Output AAAAA')
# -> [String]::Join('' , ( (87 , 114 , 105,116 , 101, 45, 79, 117 , 116 ,112, 117, 116,32 ,65,65,65 ,65 , 65) |%{ ( [CHaR] [INt]$_) } ))|.($ShellId[1]+$ShellId[13]+'x')
```