-- Description: RISCV.vhd
-- Engineer: Fearghal Morgan, Joseph Clancy, Arthur Beretta
-- National University of Ireland, Galway (NUI Galway)
--
-- Structurally connects IF, ID, EX, WB components
-- Component ctrlAndDebug controls processor execution and debug 

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity RISCV is
   Port (clk            : in  std_logic;       
         rst            : in  std_logic;
		 		 
 		-- FM TBD bit 31
		instr383downto0_Bit31s    	 : in  std_logic_vector(255 downto 0);
		useIMBit31    	 : in  std_logic;

         -- host interface
         host_memAdd    : in  std_logic_vector(31 downto 0);
		 host_memWr     : in std_logic;
         host_datToMem  : in  std_logic_vector(31 downto 0);
         host_memRd     : in std_logic;
         XX_RBOut          : out std_logic_vector(31 downto 0);
	     XX_IMOut          : out std_logic_vector(31 downto 0);
	     XX_ctrlAndDebugOut: out std_logic_vector(31 downto 0);
		 XX_forceInstrOut  : out std_logic_vector(31 downto 0);
		 XX_enPipeOut      : out std_logic;

		 -- processor - memory interface 
	     EX_MAdd        : out std_logic_vector(31 downto 0);  
		 EX_MWr         : out std_logic;  
	     EX_DToM        : out std_logic_vector(31 downto 0);  
	     EX_MRd         : out std_logic;
		 DFrM           : in  std_logic_vector(31 downto 0)
		 );
end RISCV;

architecture struct of RISCV is
signal ce             : std_logic;  
signal enPipeline     : std_logic;  

signal XX_RBArray     : RISCV_regType;

signal instruction    : std_logic_vector(31 downto 0);
signal IF_instruction : std_logic_vector(31 downto 0);

signal PC             : std_logic_vector(31 downto 0);
signal ID_PC          : std_logic_vector(31 downto 0); 
		
signal rs1D           : std_logic_vector(31 downto 0);
signal ID_rs1D        : std_logic_vector(31 downto 0);

signal rs2D           : std_logic_vector(31 downto 0);
signal ID_rs2D        : std_logic_vector(31 downto 0);

signal rd             : std_logic_vector(4 downto 0);
signal MEM_rd         : std_logic_vector(4 downto 0);

signal extImm         : std_logic_vector(31 downto 0);
signal ID_extImm      : std_logic_vector(31 downto 0);

signal DToM           : std_logic_vector(31 downto 0);

signal ALUOut         : std_logic_vector(31 downto 0);
signal EX_ALUOut      : std_logic_vector(31 downto 0);
signal MEM_ALUOut     : std_logic_vector(31 downto 0);

signal PCPlus4        : std_logic_vector(31 downto 0);
signal MEM_PCPlus4    : std_logic_vector(31 downto 0);

signal MEM_DFrM       : std_logic_vector(31 downto 0);

signal RWr            : std_logic;
signal MEM_RWr        : std_logic;

signal brAdd          : std_logic_vector(31 downto 0); 
signal MEM_brAdd      : std_logic_vector(31 downto 0); 

signal auipc          : std_logic;    
signal ID_auipc       : std_logic;    

signal selDToM        : std_logic_vector(1 downto 0);   
signal ID_selDToM     : std_logic_vector(1 downto 0);   

signal selPCSrc       : std_logic;
signal MEM_selPCSrc   : std_logic;

signal selWBD         : std_logic_vector(1 downto 0);
signal MEM_selWBD     : std_logic_vector(1 downto 0);

signal jalr           : std_logic;
signal ID_jalr        : std_logic;

signal selALUBSrc     : std_logic;
signal ID_selALUBSrc  : std_logic;

signal selALUOp       : std_logic_vector(3 downto 0);
signal ID_selALUOp    : std_logic_vector(3 downto 0);

signal selDFrM        : std_logic_vector(2 downto 0);    
signal ID_selDFrM     : std_logic_vector(2 downto 0);    

-- Signal not included in pipeline component
signal EX_selDFrM     : std_logic_vector(2 downto 0);    

signal MEM_selDFrM    : std_logic_vector(2 downto 0);    

signal WBDat  	      : std_logic_vector(31 downto 0);

signal branch         : std_logic;

signal MWr            : std_logic;
signal MRd            : std_logic;
		
begin

ctrlAndDebug_i: ctrlAndDebug 
Port map ( clk                => clk,          
           rst                => rst,          
           ce                 => ce,                       
           PC                 => PC,           
           XX_RBArray         => XX_RBArray,      
           instruction        => instruction, 
		   enPipeline         => enPipeline,
		   				 						  			
           XX_add             => host_memAdd,   
		   XX_wr              => host_memWr,  
           XX_dIn             => host_datToMem,
		   XX_rd              => host_memRd,
		   XX_ctrlAndDebugOut => XX_ctrlAndDebugOut
		);

IF_i: IF0 port map
       (clk        	          => clk,        
        rst      	          => rst, 

		-- FM TBD bit 31
		instr383downto0_Bit31s    	 => instr383downto0_Bit31s,
		useIMBit31    	 => useIMBit31, 
     	
        ce       	          => ce,        
        brAdd   	          => MEM_brAdd,   	
        selPCSrc              => MEM_selPCSrc,   
        PC                    => PC,
		PCPlus4 	          => PCPlus4, 	
		instruction           => instruction,
							  
        XX_add                => host_memAdd,   
		XX_wr                 => host_memWr,  
        XX_dIn                => host_datToMem,
		XX_rd                 => host_memRd,
		XX_IMOut              => XX_IMOut,
        XX_forceInstrOut      => XX_forceInstrOut
		);

ID_i: ID 
port map(clk                  => clk,        
        rst                   => rst,        
        ce                    => ce,         
        instruction           => IF_instruction,
        branch                => branch,     
        RWr                   => RWr,     
        MEM_RWr               => MEM_RWr, 
		rd                    => rd, 
		MEM_rd                => MEM_rd,
        rs1D                  => rs1D,       
        rs2D                  => rs2D,       
        WBDat  	              => WBDat,  	   
		extImm                => extImm,    
		selPCSrc              => selPCSrc,   
		jalr                  => jalr,       
		auipc                 => auipc,      
		selALUBSrc            => selALUBSrc, 
		selALUOp              => selALUOp,   
		selDToM               => selDToM,   
		MWr                   => MWr,     
		MRd                   => MRd,     
		selDFrM               => selDFrM,    
		selWBD                => selWBD, 
					          
		XX_RBArray            => XX_RBArray,

        XX_add                => host_memAdd,
		XX_wr                 => host_memWr, 
        XX_dIn                => host_datToMem, 
        XX_rd1                => host_memRd,
        XX_RBOut              => XX_RBOut
		);

EX_i: EX port map
       (extImm                => ID_extImm,     
		rs1D                  => ID_rs1D,       
        rs2D                  => ID_rs2D,       
        jalr                  => ID_jalr,       
        PC                    => ID_PC,         
        auipc                 => ID_auipc,      
        selALUBSrc            => ID_selALUBSrc, 
        selALUOp              => ID_selALUOp,   
        selDToM               => ID_selDToM,    
        ALUOut                => ALUOut,     
        DToM                  => DToM,       
        brAdd                 => brAdd,      
        branch                => branch     
        ); 
		
asgnMAdd_i: EX_MAdd <= EX_ALUOut;		

WB_i: WB port map
        (selWBD               => MEM_selWBD,  
		 ALUOut               => MEM_ALUOut,  
		 DFrM                 => MEM_DFrM,    
         selDFrM              => MEM_selDFrM, 
		 PCPlus4              => MEM_PCPlus4, 
         WBDat                => WBDat   
         );

pipelineTop_i: pipelineTop 
Port map (
        clk                   => clk,
        rst                   => rst,
		
        add                   => host_memAdd,
		wr                    => host_memWr, 
        dIn                   => host_datToMem, 
        rd1                   => host_memRd,
        enPipeOut             => XX_enPipeOut,
					          
        ce                    => ce,
        enPipeline            => enPipeline, 
					          
		PC                    => PC,
		ID_PC                 => ID_PC,
					          
        instruction           => instruction, 
        IF_instruction        => IF_instruction,
					      					      
		rs1D                  => rs1D,
		ID_rs1D               => ID_rs1D,
					             
		rs2D                  => rs2D,
		ID_rs2D               => ID_rs2D,
					             					      
		extImm                => extImm,
		ID_extImm             => ID_extImm,
					             
		DToM       	          => DToM,
		EX_DToM               => EX_DToM,
					             
		ALUOut                => ALUOut,
		EX_ALUOut             => EX_ALUOut,
		MEM_ALUOut            => MEM_ALUOut,
					             
		rd                    => rd,
		MEM_rd                => MEM_rd,
					          
		PCPlus4               => PCPlus4,
		MEM_PCPlus4           => MEM_PCPlus4,
					      
		DFrM      	          => DFrM,  		
		MEM_DFrM              => MEM_DFrM,
					          
		brAdd                 => brAdd,   	
		MEM_brAdd             => MEM_brAdd,
						         
        auipc                 => auipc,       
        ID_auipc              => ID_auipc,   
					             
        selDToM               => selDToM,     
        ID_selDToM            => ID_selDToM,
					             
        jalr                  => jalr,        
        ID_jalr               => ID_jalr,     
						       
	    selALUBSrc            => selALUBSrc,  
 	    ID_selALUBSrc         => ID_selALUBSrc,
						  
		selALUOp 	          => selALUOp,
		ID_selALUOp           => ID_selALUOp,
					          
		selPCSrc              => selPCSrc,
        MEM_selPCSrc          => MEM_selPCSrc,
					             
        selWBD                => selWBD,
        MEM_selWBD            => MEM_selWBD,
					             						  
        RWr                   => RWr,
        MEM_RWr               => MEM_RWr,					   
						         
		MWr                   => MWr,
		EX_MWr                => EX_MWr,
					          
   	    MRd                   => MRd,
   	    EX_MRd                => EX_MRd,
					             
		selDFrM               => selDFrM,
		MEM_selDFrM           => MEM_selDFrM
		);
		
asgnRBRegSigs_i: asgnRBRegSigs port map (XX_RBArray => XX_RBArray); -- assign x0 to x31 signals for use in vicilogic

end struct;