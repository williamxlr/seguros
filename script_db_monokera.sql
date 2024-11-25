USE [monokera]
GO
/****** Object:  Table [dbo].[Policy]    Script Date: 18/11/2024 9:31:04 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Policy](
	[policy_number] [varchar](50) NOT NULL,
	[policy_start_date] [date] NOT NULL,
	[policy_end_date] [date] NOT NULL,
	[policy_type] [varchar](50) NULL,
	[insurance_company] [varchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[policy_number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Agents]    Script Date: 18/11/2024 9:31:04 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Agents](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[policy_number] [varchar](50) NULL,
	[agent_name] [varchar](100) NULL,
	[agent_email] [varchar](100) NULL,
	[agent_phone] [varchar](20) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Insured]    Script Date: 18/11/2024 9:31:04 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Insured](
	[insured_id] [int] IDENTITY(1,1) NOT NULL,
	[policy_number] [varchar](50) NULL,
	[insured_name] [varchar](100) NULL,
	[insured_gender] [varchar](10) NULL,
	[insured_age] [int] NULL,
	[insured_address] [varchar](255) NULL,
	[insured_city] [varchar](100) NULL,
	[insured_state] [varchar](100) NULL,
	[insured_postal_code] [varchar](20) NULL,
	[insured_country] [varchar](50) NULL,
 CONSTRAINT [PK__Insured__A7628C6F4A81A129] PRIMARY KEY CLUSTERED 
(
	[insured_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  View [dbo].[Policies_Active_After_July_2023]    Script Date: 18/11/2024 9:31:04 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO




CREATE VIEW [dbo].[Policies_Active_After_July_2023] AS

SELECT 
    p.policy_number,          -- Número de póliza
    i.insured_name,          -- Nombre del asegurado
    p.policy_start_date,     -- Fecha de inicio
    p.policy_end_date,       -- Fecha de fin
    a.agent_name,            -- Nombre del agente
    a.agent_phone,           -- Teléfono del agente
    a.agent_email,           -- Email del agente
    p.insurance_company,     -- Aseguradora
    p.policy_type           -- Tipo de póliza

FROM 
    Policy p
LEFT JOIN 
    Insured i ON p.policy_number = i.policy_number
LEFT JOIN 
    Agents a ON p.policy_number = a.policy_number

WHERE 
    p.policy_end_date > '2023-07-01';  -- Filtro para incluir solo las pólizas activas después del 1 de julio de 2023
GO
/****** Object:  View [dbo].[Policies_Active_After_July_2023_Summary]    Script Date: 18/11/2024 9:31:04 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE   VIEW [dbo].[Policies_Active_After_July_2023_Summary] AS
SELECT 
    p.policy_number,          -- Número de póliza
    i.insured_name,          -- Nombre del asegurado
    p.policy_start_date,    -- Fecha de inicio
    p.policy_end_date,      -- Fecha de fin
    a.agent_name,           -- Agente
    p.insurance_company,    -- Aseguradora
    p.policy_type           -- Tipo de póliza
FROM 
    Policy p
LEFT JOIN 
    Insured i ON p.policy_number = i.policy_number
LEFT JOIN 
    Agents a ON p.policy_number = a.policy_number
WHERE 
    p.policy_end_date > '2023-07-01';  -- Filtro para incluir solo las pólizas activas después del 1 de julio de 2023


GO
/****** Object:  Table [dbo].[Claims]    Script Date: 18/11/2024 9:31:04 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Claims](
	[claim_id] [int] IDENTITY(1,1) NOT NULL,
	[policy_number] [varchar](50) NULL,
	[claim_status] [varchar](50) NULL,
	[claim_date] [date] NULL,
	[claim_amount] [decimal](18, 2) NULL,
	[claim_description] [varchar](255) NULL,
 CONSTRAINT [PK__Claims__F9CC0896E59153CE] PRIMARY KEY CLUSTERED 
(
	[claim_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Payments]    Script Date: 18/11/2024 9:31:04 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Payments](
	[payment_id] [int] IDENTITY(1,1) NOT NULL,
	[policy_number] [varchar](50) NULL,
	[payment_status] [varchar](50) NULL,
	[payment_date] [date] NULL,
	[payment_amount] [decimal](18, 2) NULL,
	[payment_method] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[payment_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Premium]    Script Date: 18/11/2024 9:31:04 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Premium](
	[premium_id] [int] IDENTITY(1,1) NOT NULL,
	[policy_number] [varchar](50) NULL,
	[premium_amount] [decimal](18, 2) NULL,
	[deductible_amount] [decimal](18, 2) NULL,
	[coverage_limit] [decimal](18, 2) NULL,
PRIMARY KEY CLUSTERED 
(
	[premium_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Agents]  WITH NOCHECK ADD  CONSTRAINT [FK__Agents__policy_n__44FF419A] FOREIGN KEY([policy_number])
REFERENCES [dbo].[Policy] ([policy_number])
GO
ALTER TABLE [dbo].[Agents] NOCHECK CONSTRAINT [FK__Agents__policy_n__44FF419A]
GO
ALTER TABLE [dbo].[Claims]  WITH NOCHECK ADD  CONSTRAINT [FK__Claims__policy_n__4222D4EF] FOREIGN KEY([policy_number])
REFERENCES [dbo].[Policy] ([policy_number])
GO
ALTER TABLE [dbo].[Claims] NOCHECK CONSTRAINT [FK__Claims__policy_n__4222D4EF]
GO
ALTER TABLE [dbo].[Insured]  WITH NOCHECK ADD  CONSTRAINT [FK__Insured__policy___398D8EEE] FOREIGN KEY([policy_number])
REFERENCES [dbo].[Policy] ([policy_number])
GO
ALTER TABLE [dbo].[Insured] NOCHECK CONSTRAINT [FK__Insured__policy___398D8EEE]
GO
ALTER TABLE [dbo].[Payments]  WITH NOCHECK ADD  CONSTRAINT [FK__Payments__policy__3F466844] FOREIGN KEY([policy_number])
REFERENCES [dbo].[Policy] ([policy_number])
GO
ALTER TABLE [dbo].[Payments] NOCHECK CONSTRAINT [FK__Payments__policy__3F466844]
GO
ALTER TABLE [dbo].[Premium]  WITH NOCHECK ADD  CONSTRAINT [FK__Premium__policy___3C69FB99] FOREIGN KEY([policy_number])
REFERENCES [dbo].[Policy] ([policy_number])
GO
ALTER TABLE [dbo].[Premium] NOCHECK CONSTRAINT [FK__Premium__policy___3C69FB99]
GO
