import React, {Component} from 'react';
import Editor from 'react-simple-code-editor';
import {highlight, languages} from 'prismjs';

import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-python';

// const code = ("def testy(x, y):\n" +
//     "  print('Hello World')");

const code = "/------------------------------------------------------------------------------\\\n" +
    "|                              Summary of Results                              |\n" +
    "\\------------------------------------------------------------------------------/\n" +
    "TestDesign\n" +
    "    + 1. test_encrypt_defined\n" +
    "    + 2. test_decrypt_defined\n" +
    "    + 3. test_find_encryption_offsets_defined\n" +
    "    + 4. test_main_defined\n" +
    "    - 5. test_docs\n" +
    "TestFunctions\n" +
    "    + 1. test_encrypt\n" +
    "    + 2. test_decrypt\n" +
    "    + 3. test_find_encryption_offsets\n" +
    "TestMain\n" +
    "    - 1. test_example_main\n" +
    "TestExtension\n" +
    "    - 1. test_extension_encrypt\n" +
    "    - 2. test_extension_autodecrypt\n" +
    "--------------------------------------------------------------------------------\n" +
    "/------------------------------------------------------------------------------\\\n" +
    "|                                 Failed Tests                                 |\n" +
    "\\------------------------------------------------------------------------------/\n" +
    "================================================================================\n" +
    "FAIL: TestDesign 5. test_docs\n" +
    "--------------------------------------------------------------------------------\n" +
    "    Traceback (most recent call last):\n" +
    "      File \"test_a1_sample.py\", line 27, in test_docs\n" +
    "        self.assertDocString(a1.encrypt)\n" +
    "    AssertionError: unexpectedly None : Documentation string is required for 'encrypt'\n" +
    "\n" +
    "================================================================================\n" +
    "FAIL: TestMain 1. test_example_main\n" +
    "--------------------------------------------------------------------------------\n" +
    "    Traceback (most recent call last):\n" +
    "      File \"test_a1_sample.py\", line 73, in test_example_main\n" +
    "        self.assertMultiLineEqual(stdio.stdout, outputs)\n" +
    "    AssertionError: '' != 'Welcome to the simple encryption tool!\\n\\[1949 chars]e!\\n'\n" +
    "    + Welcome to the simple encryption tool!\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Please enter some text to encrypt: Please enter a shift offset (1-25): The encrypted text is: fvb dpss hsdhfz yltltily aopz hz aol khf\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Please enter some text to decrypt: Please enter a shift offset (1-25): The decrypted text is: jbmo pqstu zfnach drxy i glekwv\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Please enter some text to decrypt: Please enter a shift offset (1-25): The decrypted text is: i just saw the ad and thought it looked fun\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Invalid command\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Please enter some encrypted text: Encryption offset: 1\n" +
    "    + Decrypted message: do you see those two weevils doctor\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Invalid command\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Please enter some encrypted text: Multiple encryption offsets: 4, 12, 21, 25\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Please enter some encrypted text: No valid encryption offset\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Bye!\n" +
    "\n" +
    "================================================================================\n" +
    "FAIL: TestExtension 1. test_extension_encrypt\n" +
    "--------------------------------------------------------------------------------\n" +
    "    Traceback (most recent call last):\n" +
    "      File \"test_a1_sample.py\", line 88, in test_extension_encrypt\n" +
    "        self.assertMultiLineEqual(stdio.stdout, outputs)\n" +
    "    AssertionError: '' != 'Welcome to the simple encryption tool!\\n\\[1251 chars]e!\\n'\n" +
    "    + Welcome to the simple encryption tool!\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Please enter some text to encrypt: Please enter a shift offset (1-25): The encrypted text is:\n" +
    "    +   01: bmm xf dbo ep jt tnjmf cbdl\n" +
    "    +   02: cnn yg ecp fq ku uokng dcem\n" +
    "    +   03: doo zh fdq gr lv vploh edfn\n" +
    "    +   04: epp ai ger hs mw wqmpi fego\n" +
    "    +   05: fqq bj hfs it nx xrnqj gfhp\n" +
    "    +   06: grr ck igt ju oy ysork hgiq\n" +
    "    +   07: hss dl jhu kv pz ztpsl ihjr\n" +
    "    +   08: itt em kiv lw qa auqtm jiks\n" +
    "    +   09: juu fn ljw mx rb bvrun kjlt\n" +
    "    +   10: kvv go mkx ny sc cwsvo lkmu\n" +
    "    +   11: lww hp nly oz td dxtwp mlnv\n" +
    "    +   12: mxx iq omz pa ue eyuxq nmow\n" +
    "    +   13: nyy jr pna qb vf fzvyr onpx\n" +
    "    +   14: ozz ks qob rc wg gawzs poqy\n" +
    "    +   15: paa lt rpc sd xh hbxat qprz\n" +
    "    +   16: qbb mu sqd te yi icybu rqsa\n" +
    "    +   17: rcc nv tre uf zj jdzcv srtb\n" +
    "    +   18: sdd ow usf vg ak keadw tsuc\n" +
    "    +   19: tee px vtg wh bl lfbex utvd\n" +
    "    +   20: uff qy wuh xi cm mgcfy vuwe\n" +
    "    +   21: vgg rz xvi yj dn nhdgz wvxf\n" +
    "    +   22: whh sa ywj zk eo oieha xwyg\n" +
    "    +   23: xii tb zxk al fp pjfib yxzh\n" +
    "    +   24: yjj uc ayl bm gq qkgjc zyai\n" +
    "    +   25: zkk vd bzm cn hr rlhkd azbj\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Bye!\n" +
    "\n" +
    "================================================================================\n" +
    "FAIL: TestExtension 2. test_extension_autodecrypt\n" +
    "--------------------------------------------------------------------------------\n" +
    "    Traceback (most recent call last):\n" +
    "      File \"test_a1_sample.py\", line 101, in test_extension_autodecrypt\n" +
    "        self.assertMultiLineEqual(stdio.stdout, outputs)\n" +
    "    AssertionError: '' != 'Welcome to the simple encryption tool!\\n\\[584 chars]e!\\n'\n" +
    "    + Welcome to the simple encryption tool!\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Please enter some encrypted text: Encryption offset: 15\n" +
    "    + Decrypted message: I remember him looking round the cover and whistling to himself as he did so, and then breaking out in that old sea-song that he sang so often afterwards: \"Fifteen men on the dead man's chest; Yo-ho-ho, and a bottle of rum!\"\n" +
    "    + \n" +
    "    + Please choose an option [e/d/a/q]:\n" +
    "    +   e) Encrypt some text\n" +
    "    +   d) Decrypt some text\n" +
    "    +   a) Automatically decrypt English text\n" +
    "    +   q) Quit\n" +
    "    + > Bye!\n" +
    "\n" +
    "--------------------------------------------------------------------------------\n" +
    "Ran 11 tests in 0.004 seconds with 7 passed/0 skipped/4 failed."

export class TestResults extends Component {

    state = {code};
    render() {
        return (
            <Editor
                value={this.state.code}
                onValueChange={code => this.setState({code})}
                highlight={code => highlight(code, languages.python)}
                padding={10}
                style={{
                    fontFamily: '"Fira code", "Fira Mono", monospace',
                    fontSize: 12,
                }}
            />
        )
    }

}