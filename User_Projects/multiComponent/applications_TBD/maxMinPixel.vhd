-- Description: maxMinPixel component
-- Describes most functionality in FSM, requiring less internal signals, or components

-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: 26/1/2021
-- 
-- BRAM: 32 x 256-bit words, 32 x 32-bytes (gray scale pixels)
-- Find max or min byte in BRAM

-- On completion 
--    write reg4x32_CSRA(1)(20:16) = CSSelectedXAdd(5:0)
--    write reg4x32_CSRA(1)(12:8) = CSSelectedXAdd(5:0)
--    write reg4x32_CSRA(1)(7:0)  = CSSelectedByte(7:0)
--    write reg4x32_CSRA(0)(1:0)  = 0b10, i.e, (1) = 1 => FPGA done, (0) = 0 => return control to host. Other CSRA(0) bits unchanged
--
-- Signal dictionary
--  clk					system clock strobe, rising edge active
--  rst	        		assertion (h) asynchronously clears all registers
--  ce                  chip enable, asserted high                 		 
--  go			        Assertion (H) detected in idle state to active threshold function 
--  active (Output)     Default asserted (h), except in idle state

--  reg4x32_CSRA    	4 x 32-bit Control & Status registers, also referred to as CSRA
--  reg4x32_CSRB      	32-bit Control register, CSRB
--  BRAM_dOut	        Current source memory 256-bit data  

--  wr  (Output)        Asserted to synchronously write to addressed memory
--  add (Output)  	    Addressed memory - 0b00100000 to read BRAM(255:0)
--  datToMem (Output)   32-bit data to addressed memory 

--  functBus            96-bit array of function signals, for use in debug and demonstration of function behaviour 
--  			        Not used in this example

-- Internal Signal dictionary
--  NS, CS                           finite state machine state signals 
--  NSXAdd, CSXAdd, NSYAdd, CSYAdd   next and current BRAM memory X address   
--  NSSelectedXAdd,  CSSelectedXAdd, NSSelectedYAdd,  CSSelectedYAdd  next and current selected min or max byte X address    
--    Using integer types for INTERNAL address signals, to make VHDL model more readable
--    If use std_logic_vector type, then require conversion, e.g, 
--      signal NSXAdd, CSXAdd : std_logic_vector(4 downto 0);
--      signal NSYAdd, CSYAdd : std_logic_vector(4 downto 0);
--      integer format:    to_integer( unsigned(CSXAdd) )  
--      BRAM byte slice select   
-- 	  	  using std_logic_vector type: BRAM (  (8*to_integer( unsigned(CSXAdd) ) + 7)    downto  8*to_integer( unsigned(CSXAdd) )  )
--        using integer type           BRAM (  (8*CSXAdd + 7)    downto  8*CSXAdd  )  is easier to read
--    Integer signals require conversiom if use in an assignment to a std_logic_vector signal type, e.g, generation of signal functBus(0)
--  NSSelectedByte, CSSelectedByte   next and current selected min or max byte value  

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity maxMinPixel is
    Port ( clk 		     : in STD_LOGIC;   
           rst 		     : in STD_LOGIC; 
           ce            : in  std_logic;                		 
           go            : in  std_logic;                		 
		   active        : out std_logic;

		   reg4x32_CSRA  : in array4x32; 
		   reg4x32_CSRB  : in array4x32;	
           BRAM_dOut     : in std_logic_vector(255 downto 0);	
           reg32x32_dOut : in STD_LOGIC_VECTOR(31 downto 0); -- not used in this function
					 
		   wr            : out std_logic;
		   add           : out std_logic_vector(  7 downto 0);					 
		   datToMem	     : out std_logic_vector( 31 downto 0);
		   
		   functBus      : out std_logic_vector(95 downto 0) := (others => '0')
           );
end maxMinPixel;

architecture RTL of maxMinPixel is
-- Internal signal declarations
type stateType is (idle, chkByte, writeToCSR1, writeToCSR0); -- declare enumerated state type
signal NS, CS                          : stateType; -- declare FSM state 
signal NSXAdd,         CSXAdd          : integer range 0 to 31;  
signal NSYAdd,         CSYAdd          : integer range 0 to 31;  
signal NSSelectedXAdd, CSSelectedXAdd  : integer range 0 to 31;  
signal NSSelectedYAdd, CSSelectedYAdd  : integer range 0 to 31;  
signal NSSelectedByte, CSSelectedByte  : std_logic_vector(7 downto 0);  

begin

asgnFunctBus2_i: functBus <= (others => '0'); -- not currently used 

-- FSM next state and o/p decode process
NSAndOPDec_i: process (CS, go, BRAM_dOut, reg4x32_CSRA, reg4x32_CSRB, CSXAdd, CSYAdd, CSSelectedByte, CSSelectedXAdd, CSSelectedYAdd)
begin
   NS 	 		  <= CS;     -- default signal assignments
   NSXAdd  		  <= CSXAdd; 
   NSYAdd  		  <= CSYAdd; 
   NSSelectedByte <= CSSelectedByte; 
   NSSelectedXAdd <= CSSelectedXAdd; 
   NSSelectedYAdd <= CSSelectedYAdd; 
   active    	  <= '1';    -- default asserted. Deasserted only in idle state. 
   wr   	      <= '0';
   add	          <= (others => '0'); 
   datToMem       <= (others => '0');

   case CS is 
		when idle => 			     
			active         <= '0';  
            NSXAdd         <= 0;			         -- initialise value = 0  
            NSYAdd         <= 0;			           
            NSSelectedXAdd <= 0;
            NSSelectedYAdd <= 0;
            NSSelectedByte <= X"00";                 -- default finding max byte value so start with max possible byte value 
            if go = '1' then 
			    add <= "001" & "00000";              -- BRAM word 0 address. Synchronous read BRAM(255:0)
                if reg4x32_CSRA(0)(10 downto 8) = "001" then -- finding next min byte?
                  NSSelectedByte <= X"ff";           -- finding min byte value so start with max possible byte value 
                end if;
				NS  <= chkByte;
			end if;

		when chkByte => 
		    add <= "001" & "00000"; 											   -- BRAM word 0 address. Synchronous read BRAM(255:0)
		    if reg4x32_CSRA(0)(10 downto 8) = "000" then 						   -- find next max byte
    			if BRAM_dOut( (8*CSXAdd + 7) downto 8*CSXAdd ) > CSSelectedByte then	
				   NSSelectedXAdd  <= CSXAdd;                                      -- update to new address
				   NSSelectedYAdd  <= CSYAdd;                                      
	   		  	   NSSelectedByte <= BRAM_dOut( (8*CSXAdd + 7) downto 8*CSXAdd );  -- update to new value
                end if;
		    elsif reg4x32_CSRA(0)(10 downto 8) = "001" then 				       -- find next min byte
    			if BRAM_dOut( (8*CSXAdd + 7) downto 8*CSXAdd ) < CSSelectedByte then	
				   NSSelectedXAdd  <= CSXAdd;                                      -- update to new addres
				   NSSelectedYAdd  <= CSYAdd;                                      
	   		  	   NSSelectedByte <= BRAM_dOut( (8*CSXAdd + 7) downto 8*CSXAdd );  -- update to new value
				end if;
			end if;
			
			if CSXAdd < 31 then  					                               -- all bytes in row not yet processed?           
			     NSXAdd <= CSXAdd + 1; 											   -- increment NSXAdd
			else
			     NSXAdd <= 0; 
			     NSYAdd <= CSXAdd + 1; 											   -- increment NSYAdd
			     NS <= writeToCSR1;
			end if;

		when writeToCSR1 => 
			wr       <= '1'; 
            add      <= "000" & "00001"; 										   -- reg4x32_CSRA address = 1 
		    datToMem <=   reg4x32_CSRA(1)(31 downto 24)                            -- upper 8 bits unchanged
 		                & reg4x32_CSRA(1)(23 downto 21)                            -- byte 2
 		                    & std_logic_vector( to_unsigned(CSSelectedYAdd, 5) )
			            & reg4x32_CSRA(1)(15 downto 13)                            -- byte 1
						    & std_logic_vector( to_unsigned(CSSelectedXAdd, 5) )    
						& CSSelectedByte; 										   -- byte 0
			NS       <= writeToCSR0;

		when writeToCSR0 =>     
			wr       <= '1';
            add      <= "000" & "00000"; 									       -- reg4x32_CSRA address = 0 
		    datToMem <=   reg4x32_CSRA(0)(31 downto 16)                            -- upper 16 bits unchanged 
                        & reg4x32_CSRA(0)(15 downto  8) 					       -- byte 1, bits 15:8 unchanged
                        & reg4x32_CSRA(0)( 7 downto  2) & "10"; 			       -- byte 0, bit(1) = 1 => FPGA done, bit(0) = 0 => return control to host. Bits 7:2 unchanged
			NS       <= idle;
                        
		when others => 
			null;
	end case;
end process; 

-- Synchronous process registering current FSM state value, and other registered signals
-- registers include chip enable control
stateReg_i: process (clk, rst)
begin
  if rst = '1' then 		
    CS 	           <= idle;		
    CSXAdd         <= 0; 
    CSSelectedXAdd <= 0; 
    CSSelectedYAdd <= 0; 
    CSSelectedByte <= (others => '0'); 
  elsif clk'event and clk = '1' then 
    if ce = '1' then
        CS 	           <= NS;
        CSXAdd         <= NSXAdd;
        CSSelectedXAdd <= NSSelectedXAdd;
        CSSelectedYAdd <= NSSelectedYAdd;
        CSSelectedByte <= NSSelectedByte;
     end if;
  end if;
end process; 

end RTL;