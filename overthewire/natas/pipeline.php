<?php

$ENDL = "\n";

$original_cookie=urldecode("HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg%3D");
$original_arr = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

echo "original cookie: ".$original_cookie.$ENDL.$ENDL;

$json1 =json_encode($original_arr, true);

echo "json_original:".$json1.$ENDL.$ENDL;

$xored = base64_decode($original_cookie);



function xor_encrypt($in, $key) {
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
};

//$key1 = xor_encrypt($xored, $json1);
$key1 = "eDWo";
echo "key: ".$key1.$ENDL;

echo "recovered json:".xor_encrypt($xored, $key1).$ENDL.$ENDL;

$arr1 = array( "showpassword"=>"yes", "bgcolor"=>"#fff666");
//$arr1 = $original_arr;
$cookie1 = base64_encode(xor_encrypt(json_encode($arr1), $key1));


echo "password_cookie".$cookie1.$ENDL;

$test_decrypt = xor_encrypt(base64_decode($cookie1), $key1);
echo "Test-decrypted cookie contents: $test_decrypt\n";

$curl = "curl -s --user natas11:UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk " .
        "-b \"data=$cookie1\" " .
        "\"http://natas11.natas.labs.overthewire.org\"";

echo shell_exec($curl);




// has non printable chars, but its still valid. now what we can do is