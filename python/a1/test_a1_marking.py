import inspect
import string

from functools import wraps

from testrunner import OrderedTestCase, TestMaster
from testrunner import RedirectStdIO, skipIfFailed, timeout

ALL_CHARS = string.ascii_letters + string.digits + string.punctuation

ENCRYPT = 'encrypt'
DECRYPT = 'decrypt'
FEO = 'find_encryption_offsets'
MAIN = 'main'

# If the encrypt, decrypt or find_encryption_offset functions
# prompt for input then it will fail the test (intentionally)
# will also fail if they print anything.


class TestA1(OrderedTestCase):
    @classmethod
    def setUp(cls):
        if cls.a1 is None:
            raise cls.failureException('Failed to import a1')


class TestDesign(TestA1):
    def test_clean_import(self):
        self.assertIs(getattr(self.a1, '__TEST_RUNNER_CLEAN_IMPORT'), True)

    def test_defined(self):
        self.aggregate(self.assertFunctionDefined, self.a1, ENCRYPT, 2, tag=ENCRYPT)
        self.aggregate(self.assertFunctionDefined, self.a1, DECRYPT, 2, tag=DECRYPT)
        self.aggregate(self.assertFunctionDefined, self.a1, FEO, 1, tag=FEO)
        self.aggregate(self.assertFunctionDefined, self.a1, MAIN, 0, tag=MAIN)

        self.aggregate_tests()

    def test_documentation(self):
        self.aggregate(self.assertDocString, self.a1, ENCRYPT)
        self.aggregate(self.assertDocString, self.a1, DECRYPT)
        self.aggregate(self.assertDocString, self.a1, FEO)
        self.aggregate(self.assertDocString, self.a1, MAIN)

        self.aggregate_tests()


class TestEncrypt(TestA1):
    def test_sample(self):
        encrypt = getattr(self.a1, self.guess_function_name(self.a1, ENCRYPT))
        with RedirectStdIO(stdin=True, stdout=True) as stdio:
            try:
                self.assertEqual(encrypt("you will always remember this as the day", 7),
                                 'fvb dpss hsdhfz yltltily aopz hz aol khf')
                self.assertEqual(encrypt("music is the shorthand of emotion", 2),
                                 'owuke ku vjg ujqtvjcpf qh goqvkqp')
                self.assertEqual(encrypt("qgnrag hgorkey gtj cnovvkj ixkgs", 9),
                                 'zpwajp qpxatnh pcs lwxeets rgtpb')

            except EOFError:
                self.fail(msg=f"{ENCRYPT} function should not prompt for input")

        self.assertEqual(stdio.stdout, '',
                         msg=f"{ENCRYPT} function should not be printing")

    def test_lower_no_overflow(self):
        encrypt = getattr(self.a1, self.guess_function_name(self.a1, ENCRYPT))
        with RedirectStdIO(stdin=True, stdout=True):
            try:
                self.assertEqual(encrypt('mno', 1), 'nop')
            except EOFError:
                self.fail(msg=f"{ENCRYPT} function should not prompt for input")

    @skipIfFailed(test_name="test_lower_no_overflow")
    def test_lower_overflow(self):
        encrypt = getattr(self.a1, self.guess_function_name(self.a1, ENCRYPT))
        self.assertEqual(encrypt('xyz', 25), 'wxy')

    def test_upper_no_overflow(self):
        encrypt = getattr(self.a1, self.guess_function_name(self.a1, ENCRYPT))
        with RedirectStdIO(stdin=True, stdout=True):
            try:
                self.assertEqual(encrypt('MNO', 1), 'NOP')
            except EOFError:
                self.fail(msg=f"{ENCRYPT} function should not prompt for input")

    @skipIfFailed(test_name="test_upper_no_overflow")
    def test_upper_overflow(self):
        encrypt = getattr(self.a1, self.guess_function_name(self.a1, ENCRYPT))
        self.assertEqual(encrypt('XYZ', 25), 'WXY')

    @skipIfFailed(test_name="test_lower_no_overflow")
    @skipIfFailed(test_name="test_upper_no_overflow")
    def test_mixed_overflow(self):
        encrypt = getattr(self.a1, self.guess_function_name(self.a1, ENCRYPT))
        self.assertEqual(encrypt('xXyYzZ', 25), 'wWxXyY')

    @skipIfFailed(test_name="test_lower_no_overflow")
    @skipIfFailed(test_name="test_upper_no_overflow")
    def test_complex(self):
        encrypt = getattr(self.a1, self.guess_function_name(self.a1, ENCRYPT))
        self.assertEqual(encrypt(ALL_CHARS, 13),
                         'nopqrstuvwxyzabcdefghijklm'
                         'NOPQRSTUVWXYZABCDEFGHIJKLM'
                         '0123456789!"#$%&\'()*+,-./'
                         ':;<=>?@[\\]^_`{|}~')

    def test_zero_offset(self):
        encrypt = getattr(self.a1, self.guess_function_name(self.a1, ENCRYPT))
        with RedirectStdIO(stdin=True, stdout=True) as stdio:
            try:
                self.assertEqual(encrypt("you will always remember this as the day", 0),
                                 'you will always remember this as the day')
            except EOFError:
                self.fail(msg="encrypt function should not prompt for input")

        self.assertEqual(stdio.stdout, '',
                         msg="encrypt function should not be printing")


class TestDecrypt(TestA1):
    def test_sample(self):
        decrypt = getattr(self.a1, self.guess_function_name(self.a1, DECRYPT))
        with RedirectStdIO(stdin=True, stdout=True) as stdio:
            try:
                self.assertEqual(decrypt("a bmkl kso lzw sv sfv lzgmyzl al dggcwv xmf", 17),
                                 'j kvtu tbx uif be boe uipvhiu ju mpplfe gvo')
                self.assertEqual(decrypt("a bmkl kso lzw sv sfv lzgmyzl al dggcwv xmf", 18),
                                 'i just saw the ad and thought it looked fun')
                self.assertEqual(decrypt("asdf ghjkl qwerty uiop z xcvbnm", 17),
                                 'jbmo pqstu zfnach drxy i glekwv')
            except EOFError:
                self.fail(msg=f"{DECRYPT} function should not prompt for input")

        self.assertEqual(stdio.stdout, '',
                         msg=f"{DECRYPT} function should not be printing")

    def test_lower_no_overflow(self):
        decrypt = getattr(self.a1, self.guess_function_name(self.a1, DECRYPT))
        with RedirectStdIO(stdin=True, stdout=True):
            try:
                self.assertEqual(decrypt('mno', 1), 'lmn')
            except EOFError:
                self.fail(msg=f"{DECRYPT} function should not prompt for input")

    @skipIfFailed(test_name="test_lower_no_overflow")
    def test_lower_overflow(self):
        decrypt = getattr(self.a1, self.guess_function_name(self.a1, DECRYPT))
        self.assertEqual(decrypt('abc', 25), 'bcd')

    def test_upper_no_overflow(self):
        decrypt = getattr(self.a1, self.guess_function_name(self.a1, DECRYPT))
        with RedirectStdIO(stdin=True, stdout=True):
            try:
                self.assertEqual(decrypt('MNO', 1), 'LMN')
            except EOFError:
                self.fail(msg=f"{DECRYPT} function should not prompt for input")

    @skipIfFailed(test_name="test_upper_no_overflow")
    def test_upper_overflow(self):
        decrypt = getattr(self.a1, self.guess_function_name(self.a1, DECRYPT))
        self.assertEqual(decrypt('ABC', 25), 'BCD')

    @skipIfFailed(test_name="test_lower_no_overflow")
    @skipIfFailed(test_name="test_upper_no_overflow")
    def test_mixed_overflow(self):
        decrypt = getattr(self.a1, self.guess_function_name(self.a1, DECRYPT))
        self.assertEqual(decrypt('aAbBcC', 25), 'bBcCdD')

    @skipIfFailed(test_name="test_lower_no_overflow")
    @skipIfFailed(test_name="test_upper_no_overflow")
    def test_complex(self):
        decrypt = getattr(self.a1, self.guess_function_name(self.a1, DECRYPT))
        self.assertEqual(decrypt('nopqrstuvwxyzabcdefghijklm'
                                 'NOPQRSTUVWXYZABCDEFGHIJKLM'
                                 '0123456789!"#$%&\'()*+,-./'
                                 ':;<=>?@[\\]^_`{|}~', 13), ALL_CHARS)

    def test_zero_offset(self):
        decrypt = getattr(self.a1, self.guess_function_name(self.a1, DECRYPT))
        with RedirectStdIO(stdin=True, stdout=True) as stdio:
            try:
                self.assertEqual(decrypt("a bmkl kso lzw sv sfv lzgmyzl al dggcwv xmf", 0),
                                 'a bmkl kso lzw sv sfv lzgmyzl al dggcwv xmf')
            except EOFError:
                self.fail(msg="encrypt function should not prompt for input")

        self.assertEqual(stdio.stdout, '',
                         msg="encrypt function should not be printing")


@timeout(1.5)
class TestFindEncryptionOffsets(TestA1):
    def test_sample(self):
        feo = getattr(self.a1, self.guess_function_name(self.a1, FEO))
        with RedirectStdIO(stdin=True, stdout=True) as stdio:
            try:
                self.assertEqual(feo("iynjo fuhsudj ev jxu jycu yj mehai qbb jxu jycu"), (16,))
                self.assertEqual(feo("vftg amnl aqkkxmn mjmcqlm emkveoxtmn lvbmlomz"), ())
                self.assertEqual(feo("nmd"), (4, 12, 21, 25))

            except EOFError:
                self.fail(msg=f"{FEO} function should not prompt for input")

        self.assertEqual(stdio.stdout, '', msg=f"{FEO} function should not be printing")

    @skipIfFailed(test_name='test_sample')
    def test_lower_vs_upper(self):
        feo = getattr(self.a1, self.guess_function_name(self.a1, FEO))
        lower_offsets = feo('lipps asvph')
        upper_offsets = feo('LIPPS ASVPH')
        self.assertEqual(lower_offsets, upper_offsets)

    @skipIfFailed(test_name='test_sample')
    def test_contractions_ignored(self):
        feo = getattr(self.a1, self.guess_function_name(self.a1, FEO))
        self.assertEqual(feo("ai'vi ksswi'h"), tuple(range(1, 26)))

    @skipIfFailed(test_name='test_sample')
    def test_hyphens(self):
        feo = getattr(self.a1, self.guess_function_name(self.a1, FEO))
        self.assertEqual(feo('hskw-evi-xli-fiwx'), (4,))

    @skipIfFailed(test_name='test_sample')
    def test_ignores_punctuation(self):
        feo = getattr(self.a1, self.guess_function_name(self.a1, FEO))
        self.assertEqual(feo(
            '!e "ee eel# e$elih eelmr%k &eelw e(ep eep)mm *eepmmw ee+pw '
            'eevhzev,o eevhze.vow eev/haspj eevh:aspziw ;eevkl eevvk<l '
            'eevvk=ll >eevxm eevxm?w ee@w eew[zskip eewzs\\kipw e]f '
            'e^fe _efeg efege` ef{egew efeg|m efeg}o efeg~w'), (4,))

    @skipIfFailed(test_name='test_sample')
    def test_complex(self):
        feo = getattr(self.a1, self.guess_function_name(self.a1, FEO))
        self.assertEqual(feo(
            '£e ee¤ e¥el ee¦lih eelmrk§ e¨elw eep© eepmm« eep¬mmw '
            'eepw\xad ®eevhzevo ee¯vhzevow eevhasp°j eevhaspz±iw ee²vkl '
            'eevv³kl eevvkl´l ¶eevxm eevxmw· ee¸w e¹ewzskip e»ewzskipw '
            '¼ef ef½e ef¾eg ¿efege ×efegew ef÷egm'), (4,))


@timeout(1)
class TestMain(TestA1):
    def test_sample(self):
        _main = getattr(self.a1, self.guess_function_name(self.a1, MAIN))
        with open('data_files/sample_main.in') as fin, \
                open('data_files/sample_main.out') as fout:
            inputs = fin.read()
            outputs = fout.read()

        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(inputs)
            _main()

        self.assertMultiLineEqual(stdio.stdinout, outputs, strip=True)

    def test_encrypt(self):
        _main = getattr(self.a1, self.guess_function_name(self.a1, MAIN))
        with open('data_files/encrypt.in') as fin, \
                open('data_files/encrypt.out') as fout:
            inputs = fin.read()
            outputs = fout.read()

        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(inputs)
            _main()

        self.assertMultiLineEqual(stdio.stdinout, outputs, strip=True)

    def test_decrypt(self):
        _main = getattr(self.a1, self.guess_function_name(self.a1, MAIN))
        with open('data_files/decrypt.in') as fin, \
                open('data_files/decrypt.out') as fout:
            inputs = fin.read()
            outputs = fout.read()

        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(inputs)
            _main()

        self.assertMultiLineEqual(stdio.stdinout, outputs, strip=True)

    def test_invalid(self):
        _main = getattr(self.a1, self.guess_function_name(self.a1, MAIN))
        with open('data_files/invalid.in') as fin, \
                open('data_files/invalid.out') as fout:
            inputs = fin.read()
            outputs = fout.read()

        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(inputs)
            _main()

        self.assertMultiLineEqual(stdio.stdinout, outputs, strip=True)

    def test_extension_autodecrypt_sample(self):
        _main = getattr(self.a1, self.guess_function_name(self.a1, MAIN))
        with open('data_files/sample_ext_a.in') as fin, \
                open('data_files/sample_ext_a.out') as fout:
            inputs = fin.read()
            output = fout.read()

        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(inputs)
            _main()

        self.assertMultiLineEqual(stdio.stdinout, output, strip=True)

    def test_extension_encrypt_zero_sample(self):
        _main = getattr(self.a1, self.guess_function_name(self.a1, MAIN))
        with open('data_files/sample_ext_e_zero.in') as fin, \
                open('data_files/sample_ext_e_zero.out') as fout, \
                open('data_files/sample_ext_e_zero.back.out') as fout_back:
            inputs = fin.read()
            output = fout.read()
            output_back = fout_back.read()

        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(inputs)
            _main()

        backup_failed = False
        try:
            self.assertMultiLineEqual(stdio.stdinout, output_back, strip=True)
        except AssertionError:
            backup_failed = True

        if backup_failed:
            self.assertMultiLineEqual(stdio.stdinout, output, strip=True)

    def test_extension_decrypt_zero(self):
        _main = getattr(self.a1, self.guess_function_name(self.a1, MAIN))
        with open('data_files/ext_d_zero.in') as fin, \
                open('data_files/ext_d_zero.out') as fout, \
                open('data_files/ext_d_zero.back.out') as fout_back:
            inputs = fin.read()
            output = fout.read()
            output_back = fout_back.read()

        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(inputs)
            _main()

        backup_failed = False
        try:
            self.assertMultiLineEqual(stdio.stdinout, output_back, strip=True)
        except AssertionError:
            backup_failed = True

        if backup_failed:
            self.assertMultiLineEqual(stdio.stdinout, output, strip=True)

    def test_not_recursive(self):
        _main = getattr(self.a1, self.guess_function_name(self.a1, MAIN))

        with open('data_files/recursive.in') as fin:
            inputs = fin.read()

        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(inputs)
            self.assertIsNotRecursive(_main)


class TestExtra(TestA1):
    def test_decrypt_calls_another(self):
        """
        decorates all methods of a1 except decrpyt counting
        number of function calls for each. pass if at least one
        function is called once.
        """
        decrypt = getattr(self.a1, self.guess_function_name(self.a1, DECRYPT))

        attrs = {k: v for k, v in inspect.getmembers(
            self.a1, predicate=inspect.isfunction) if v != decrypt}
        calls = {k: 0 for k in attrs}

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal calls
                calls[func.__name__] += 1
                return func(*args, **kwargs)
            return wrapper

        for key, value in attrs.items():
            setattr(self.a1, key, decorator(value))

        with RedirectStdIO(stdin=True, stdout=True) as stdio:
            try:
                decrypt("xyz", 1)
            except EOFError:
                self.fail(msg=f"{ENCRYPT} function should not prompt for input")
            finally:
                for key, value in attrs.items():
                    setattr(self.a1, key, value)

        self.assertEqual(stdio.stdout, '',
                         msg=f"{ENCRYPT} function should not be printing")
        self.assertIn(1, calls.values(), msg=f"{DECRYPT} does not call another function once")

    def test_feo_calls_encrypt_or_decrypt(self):
        encrypt_name = self.guess_function_name(self.a1, ENCRYPT)
        decrypt_name = self.guess_function_name(self.a1, DECRYPT)

        encrypt = getattr(self.a1, encrypt_name)
        decrypt = getattr(self.a1, decrypt_name)
        feo = getattr(self.a1, self.guess_function_name(self.a1, FEO))

        called = False

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal called
                called = True
                return func(*args, **kwargs)
            return wrapper

        setattr(self.a1, encrypt_name, decorator(encrypt))
        setattr(self.a1, decrypt_name, decorator(decrypt))

        with RedirectStdIO(stdin=True, stdout=True) as stdio:
            try:
                feo("xyz")
            except EOFError:
                self.fail(msg=f"{FEO} function should not prompt for input")
            finally:
                setattr(self.a1, encrypt_name, encrypt)
                setattr(self.a1, decrypt_name, decrypt)

        self.assertEqual(stdio.stdout, '', msg=f"{FEO} function should not be printing")
        self.assertIs(called, True, msg=f"{FEO} does not call {ENCRYPT}/{DECRYPT}")


def main():
    test_cases = [
        TestDesign,
        TestEncrypt,
        TestDecrypt,
        TestFindEncryptionOffsets,
        TestMain,
        # TestExtra
    ]

    master = TestMaster(timeout=0.2,
                        scripts=[('a1', 'a1.py')])
    master.run(test_cases)


if __name__ == '__main__':
    main()