-N":"
-P":unicorns"
-D":1999/01/01"
-p":?'Enter password: '"
{=pP
  -v":You got the password correct!"
  <v
  -d":?'To confirm your identity, enter your date of birth (YYYY/MM/DD): '"
  {=dD
    -v":Logging in..."
    <v
  }|
  {!dD
    -v":Login failed."
    <v
  }|

}|
{!pP
  -v":Incorrect password!"
  <v
}|
<N
