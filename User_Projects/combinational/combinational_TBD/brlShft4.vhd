-- Engineer: Fearghal Morgan
-- viciLogic 
-- Creation Date: 1/10/2014
-- brlShft4: Barrel shifter 

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity brlShft4 is
    Port ( numShft    : in  std_logic_vector(1 downto 0);
		   brlShftIn  : in  std_logic_vector(3 downto 0);
           brlShftOut : out std_logic_vector(3 downto 0)
           );
end brlShft4;

architecture comb of brlShft4 is
begin

brlShft4_i: process(numShft, brlShftIn) 
begin
	brlShftOut     <= brlShftIn; -- default, no bit shift 
	if     numShft = "01" then 
    	brlShftOut <= brlShftIn(2 downto 0) & brlShftIn(3);  
  	elsif  numShft = "10" then 
        brlShftOut <= brlShftIn(1 downto 0) & brlShftIn(3 downto 2);  
  	elsif  numShft = "11" then 
		brlShftOut <= brlShftIn(0)          & brlShftIn(3 downto 1);  
	end if;
end process;

end comb;