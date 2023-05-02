-- Description: 7-segment decoder, with high asserted outputs 
-- Authors: Fearghal Morgan
-- Date: 2/10/2014
-- Change History: Initial version

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.ALL;

entity dec7Seg is
    Port ( dec7SegIn  : in std_logic_vector(3 downto 0); -- input digit (4 bits)
           dec7SegOut : out std_logic_vector(6 downto 0) -- decoded output
           -- with 7-segment LED bit index (0-7) or letter index (a-g) labelled in brackets
           --     ==(0)==              ==(a)==
           --    =       =            =       = 
           --   (5)     (1)          (f)     (b) 
           --    =       =            =       = 
           --     ==(6)==              ==(g)==
           --    =       =            =       = 
           --   (4)     (2)          (e)     (c) 
           --    =       =            =       = 
           --     ==(3)==              ==(d)==
         );
         
end dec7Seg;

architecture comb of dec7Seg is
-- viciLogic-related signal declarations == START
signal dec7SegInIndex : std_logic_vector(15 downto 0);
-- viciLogic-related signal declarations == END
begin

-- viciLogic-related signal assignment == START
dec7SegInIndex_i: process(dec7SegIn)
begin
	dec7SegInIndex <= (others => '0'); -- default
    for i in 0 to 15 loop
	  if to_integer(unsigned(dec7SegIn)) = i then
		dec7SegInIndex(i) <= '1'; 
	  end if;
	end loop;
end process;
-- viciLogic-related signal assignment == END

dec7Seg_i: process (dec7SegIn)
begin
  dec7SegOut <= "0111111"; 				      -- default
  case dec7SegIn is 
      when "0001" => dec7SegOut <= "0000110"; -- 1
      when "0010" => dec7SegOut <= "1011011"; -- 2
      when "0011" => dec7SegOut <= "1001111"; -- 3
      when "0100" => dec7SegOut <= "1100110"; -- 4
      when "0101" => dec7SegOut <= "1101101"; -- 5
      when "0110" => dec7SegOut <= "1111101"; -- 6
      when "0111" => dec7SegOut <= "0000111"; -- 7
      when "1000" => dec7SegOut <= "1111111"; -- 8
      when "1001" => dec7SegOut <= "1101111"; -- 9
      when "1010" => dec7SegOut <= "1110111"; -- A
      when "1011" => dec7SegOut <= "1111100"; -- B
      when "1100" => dec7SegOut <= "0111001"; -- C
      when "1101" => dec7SegOut <= "1011110"; -- D
      when "1110" => dec7SegOut <= "1111001"; -- E
      when "1111" => dec7SegOut <= "1110001"; -- F
      when others => null; 
  end case;
end process;
end comb;