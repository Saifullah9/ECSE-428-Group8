Feature: Log In

As a SupplyHero user
I want to login to my user account
So that I can access my SupplyHero account services

  Scenario Outline: Login to Account (Normal Flow)
  
    Given user has user has created an account with <email> and <password>
    When user has requested to login with their correct <email> and <password>
    Then the <email> and <password> information is correct
    And the user has logged in successfully

    Examples:
      |email		    	    	| password	    |
      |parent@hotmail.com 	        | a!s@d#	    |
      |child@hotmail.com 		    | asd!@#	    |

     
  Scenario Outline: Fail to Login (Error Flow)
  
    Given user has user has created an account with <email> and <password>
    When user has requested to login with their <bad_email> and <bad_password>
    And the <bad_email> and <bad_password> information is incorrect
    Then a "Invalid Email/Password." message is shown

    Examples:
      |email		    		    | password	 |  bad_email            | bad_password     |
      |parent@hotmail.com 	        | blahblah	 |  parent@hotmail.ca    | blahblah         |
      |parent@hotmail.com 	        | blahblah	 |  parent@hotmail.com   | blah             |






