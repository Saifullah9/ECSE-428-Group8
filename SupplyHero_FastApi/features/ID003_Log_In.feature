Feature: Log In

As a SupplyHero user
I want to login to my user account
So that I can access my SupplyHero account services

  Scenario: Login to Account (Normal Flow)
  
    Given user has an existing account
     When user has requested to login with their <email> and <password>
     And <email> and <password> information is correct
     Then user is logged in
     
    |email		    	    	| password	 | 
    |parent@hotmail.com 	| a!s@d#	   | 
    |child@hotmail.com 		| asd!@#	   | 

     
  Scenario: Fail to Login (Error Flow)
  
    Given user has an existing account
     When user has entered their following login information
    |Email		    		    | Password	 | 
    |parent@hotmail.com 	| blahblah	 |
     And login information is incorrect
     Then a "Invalid Email/Password." message is shown




