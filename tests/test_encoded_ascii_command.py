import random
from invoke_obfuscation.encoded_ascii_command import EncodedAsciiCommand


def check_all_different(results):
    # check all results are different
    return len(set(results)) == len(results)

def test_results_are_different():
    results = []
    for _ in range(10):
        results.append(EncodedAsciiCommand.invoke('Write-Output TESUYA'))
    
    assert check_all_different(results) is True

def test_random_parameter():
    results = []
    for _ in range(10):
        base_script_ptn = random.choice([1, 2, 3])
        invoke_expression_ptn = random.choice([1, 2, 3])
        invoke_ptn = random.choice([1, 2])
        results.append(EncodedAsciiCommand.invoke(
            'Write-Output TESUYA',
            base_script_ptn=base_script_ptn,
            invoke_expression_ptn=invoke_expression_ptn,
            invoke_ptn=invoke_ptn))

    assert check_all_different(results) is True