-- Component: memory_top 
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: 26/1/2021

-- Description
-- includes four memory components
--   BRAM, a 32 x 256-bit block RAM, supporting synchronous writes and reads
--      BRAM is synchronously written on rising clk edge   
--      BRAM is synchronously read    on falling clk edge  
--   Three register memories, each with asynchronous reset, synchronous load 0, and synchronous write enable (all high asserted)
-- 		reg4x32_CSRA 
--         4 x 32-bit register memory, with additional clr00 input control signal. Assertion (h) synchronously clears reg4x32_CSRA(0)(0) bit
--      reg32x32  
--		   32 x 32-bit register memory
--      reg4x32_CSRB      
--         4 x 32-bit register memory
-- Provides write/read access to / from memory components

-- selDSPOrHostCtrl component  	selects *memWr, *memAdd, *datToMem data path
--                              if reg4x32_CSRA(0)(0) is asserted, DSP_top is master, else host is master 
-- 	                            reg4x32_CSRB is accessible by host at all time and is not controlled by reg4x32_CSRA(0)(0)
-- decodeMemWr component	    on asserton of *memWr, decodes memAdd(7:5) to select memory component to be written
-- selDatToHost	component		decodes memAdd(7:5) to select memory component to be read


-- Signal dictionary 
-- clk  	                     system clock strobe, rising edge active 
-- rst                           assertion (h) asynchronously clears CSR and result register arrays (though not BRAM)  			        
-- host memory interface signals 		
--  host_memWr                   assertion writes memory(add) = datToMem
--  host_memAdd               
--       host_memAdd(11:8)       selects source memory 32-bit word (000 => word 0 bits 31:0, 111 => word 7 bits 255:224) 
--       host_memAdd(7:5)        memory bank select  
--  host_datToMem             
-- DSP memory interface signals
--  DSP_memWr                    assertion writes memory(add) = datToMem
--  DSP_memAdd               
--  DSP_datToMem             
-- datToHost                     32-bit data read by host  
--                                  synchronously returns all DSP function finite state machines to idle state : in std_logic;   
-- 							     	synchronously clears CSR(0)(0) to return control to host, asserts (CSR(3)(31) status bit) 
-- memory data output
-- BRAM_dOut					 32-bit data selected from BRAM(31:0)(255:0)
-- reg32x32_dOut			     32-bit data selected from reg32x32(31:0)(31:0)
-- reg4x32_CSRA			         4 x 32-bit data array, reg4x32_clr(3:0)(31:0)
-- reg4x4_CSRB_dOut				 32-bit data selected from reg4x32(3:0)(31:0) 

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity memory_top is 
    Port (  clk  	      : in  STD_LOGIC;
            rst           : in  STD_LOGIC;
			            			  
	        host_memWr    : in  std_logic;
	        host_memAdd   : in  std_logic_vector(10 downto 0);
		    host_datToMem : in  std_logic_vector(255 downto 0);
			
	        DSP_memWr     : in  std_logic;
	        DSP_memAdd    : in  std_logic_vector(7 downto 0);
		    DSP_datToMem  : in  std_logic_vector(31 downto 0);
		    
		    DSP_functBus  : in  std_logic_vector(95 downto 0);
						  
 	 	    datToHost     : out std_logic_vector(31 downto 0);
						  
			BRAM_dOut     : out std_logic_vector(255 downto 0);
			reg32x32_dOut : out std_logic_vector(31 downto 0);
			
			reg4x32_CSRA  : out array4x32;
			reg4x32_CSRB  : out array4x32
		 );
end memory_top;

architecture struct of memory_top is
signal memWr               : std_logic;
signal memAdd              : std_logic_vector( 10 downto 0);
signal datToMem            : std_logic_vector(255 downto 0);

signal BRAM_we             : std_logic;
signal reg32x32_we         : std_logic;
signal reg4x32_CSRA_we     : std_logic;
signal reg4x32_CSRB_we     : std_logic;

signal DSPMaster   	       : std_logic;

signal XX_intBRAM32x256_dOut  : std_logic_vector(255 downto 0);

signal XX_intReg32x32_dOut : std_logic_vector(31 downto 0);

signal XX_intReg4x32_CSRA  : array4x32;
signal reg4x32_CSRA_dOut   : std_logic_vector(31 downto 0);

signal XX_intReg4x32_CSRB  : array4x32;
signal reg4x32_CSRB_dOut   : std_logic_vector(31 downto 0);

signal ld0_reg4x32_CSRA    : std_logic;
signal ld0_reg32x32        : std_logic;

signal clr00_reg4x32_CSRA  : std_logic;

signal memAdd7DT5          : std_logic_vector(2 downto 0);
signal memAdd4DT0          : std_logic_vector(4 downto 0);
signal host_memAdd7DT5     : std_logic_vector(2 downto 0);

begin

asgnMemAdd_7DT5_i: memAdd7DT5 <= memAdd(7 downto 5);
asgnMemAdd_4DT0_i: memAdd4DT0 <= memAdd(4 downto 0); 
asgn_host_memAdd_7DT5_i: host_memAdd7DT5 <= host_memAdd(7 downto 5);

-- Assign output signals
asgnBRAM_dOut_i:          BRAM_dOut     <= XX_intBRAM32x256_dOut;
asgnReg32x32_dOut_i:      reg32x32_dOut <= XX_intReg32x32_dOut;
asgnReg4x32_CSRA_i:       reg4x32_CSRA  <= XX_intReg4x32_CSRA;
asgnReg4x32_CSRB_i:       reg4x32_CSRB  <= XX_intReg4x32_CSRB;
asgnDSPMaster_i:          DSPMaster     <= XX_intReg4x32_CSRA(0)(0);

asgn_ld0_reg4x32_CSRA_i:   ld0_reg4x32_CSRA   <= XX_intReg4x32_CSRB(0)(2);
asgn_ld0_reg32x32_i: 	   ld0_reg32x32       <= XX_intReg4x32_CSRB(0)(1);
asgn_CSRA_reg4x32_CSRA_i:  clr00_reg4x32_CSRA <= XX_intReg4x32_CSRB(0)(0);

selDSPOrHostCtrl_i: selDSPOrHostCtrl            
Port map ( DSPMaster      => DSPMaster,  

	       host_memWr     => host_memWr,   
	       host_memAdd    => host_memAdd,  
		   host_datToMem  => host_datToMem,
		   
	       DSP_memWr      => DSP_memWr,    
	       DSP_memAdd     => DSP_memAdd,   
		   DSP_datToMem   => DSP_datToMem, 			 		 
		   
	       memWr          => memWr,             
	       memAdd         => memAdd,            
		   datToMem       => datToMem          
           );

decodeMemWr_i: decodeMemWr 
Port map ( memWr            => memWr,       
	       memAdd           => memAdd,      
           BRAM_we          => BRAM_we, 
		   reg32x32_we      => reg32x32_we,       
           reg4x32_CSRA_we  => reg4x32_CSRA_we,

           host_memWr       => host_memWr,
           host_memAdd      => host_memAdd,
           reg4x32_CSRB_we  => reg4x32_CSRB_we
 		 );
		 
selDatToHost_i: selDatToHost
Port map ( memAdd               => memAdd,
		   reg4x32_CSRA_dOut    => reg4x32_CSRA_dOut,
		   XX_intBRAM32x256_dOut=> XX_intBRAM32x256_dOut,       
		   XX_intReg32x32_dOut  => XX_intReg32x32_dOut,  
		   reg4x32_CSRB_dOut    => reg4x32_CSRB_dOut,
		   datToHost            => datToHost	   
 		 );

-- ============== instantiate memory components

BRAM32x256_i: BRAM32x256
Port map ( clk  => clk, 
           we   => BRAM_we,     
	       add  => memAdd(4 downto 0),   
	       dIn  => datToMem,   
           dOut => XX_intBRAM32x256_dOut
 		 );

reg32x32_i: reg32x32 
Port map ( clk  => clk, 
           rst  => rst, 
           ld0  => ld0_reg32x32,  	
           we   => reg32x32_we,  
	       add  => memAdd(4 downto 0), 
	       dIn  => datToMem(31 downto 0), 	  
           reg  => open,
           dOut => XX_intReg32x32_dOut
 		 );

reg4x32_CSRA_c_i: reg4x32_CSRA_c
Port map ( clk  => clk, 
           rst  => rst, 
     	   clr00=> clr00_reg4x32_CSRA, 
           ld0  => ld0_reg4x32_CSRA, 		   
           we   => reg4x32_CSRA_we,  
	       add  => memAdd(1 downto 0), 
	       dIn  => datToMem(31 downto 0), 	  
           reg  => XX_intReg4x32_CSRA, 
           dOut => reg4x32_CSRA_dOut
 		 );

reg4x32_CSRB_c_i: reg4x32_CSRB_c 
Port map ( clk  => clk, 
           rst  => rst, 
           ld0  => '0', 	 	
           we   => reg4x32_CSRB_we,  
	       add  => memAdd(1 downto 0), 
	       dIn3DT1 => DSP_functBus, 	  
	       dIn => datToMem(31 downto 0), 	  
           reg => XX_intReg4x32_CSRB, 
           dOut => reg4x32_CSRB_dOut
 		 );
		 		           
end struct;