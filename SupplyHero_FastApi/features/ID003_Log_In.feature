Feature: Log In

As a SupplyHero user
I want to login to my user account
So that I can access my SupplyHero account services

  Scenario Outline: Login to Account (Normal Flow)
  
    Given user has user has created an account with <email> and <password>
    When user has requested to login with their <email> and <password>
    Then the <email> and <password> information is correct
    And the user has logged in successfully

    Examples:
      |email		    	    	| password	    |
      |parent@hotmail.com 	        | a!s@d#	    |
      |child@hotmail.com 		    | asd!@#	    |

     
  Scenario Outline: Fail to Login (Error Flow)
  
    Given user has user has created an account with <email> and <password>
    When user has requested to login with their incorrect <bad_email> or <bad_password>
    Then the <bad_email> and <bad_password> information is incorrect
    And an "Invalid Email/Password." message is shown

    Examples:
      | email		    		    | password	 | bad_email            | bad_password     |
      | dad@hotmail.com 	        | blahblah	 | dad@hotmail.ca       | blahblah         |
      | dad@hotmail.com 	        | blahblah	 | dad@hotmail.com      | blah             |






