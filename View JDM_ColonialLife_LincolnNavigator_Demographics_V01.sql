USE [Millennium]
GO

/****** Object:  View [dbo].[JDM_ColonialLife_LincolnNavigator_Demographics_V01]    Script Date: 9/11/2025 9:10:09 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


ALTER View [dbo].[JDM_ColonialLife_LincolnNavigator_Demographics_V01] AS

SELECT c.co,
	e.ssn AS [Employee SSN]
	,e.lastname
	,e.firstname
	,e.birthDate
	,e.sex
	,e.hireDate
	,dbo.JDM_GetAnnualSalary(e.co,e.id) AS annualSalary
	,e.address1
	,e.address2
	,e.city
	,e.state
	,e.zip
	,e.title
	,ISNULL(d1.name,'') AS cc1
	,ISNULL(d2.name,'') AS cc2
	,ISNULL(d3.name,'') AS cc3
	,ISNULL(d4.name,'') AS cc4
	,ISNULL(d5.name,'') AS cc5
	,ISNULL(REPLACE(e.emailaddresspersonal,'',NULL),e.emailaddress) AS emailAddress
	,e.homePhone
FROM cinfo c
	JOIN einfo e ON c.co=e.co 
	LEFT OUTER JOIN CDept1 d1 ON e.co=d1.co AND e.cc1=d1.cc1 
	LEFT OUTER JOIN CDept2 d2 ON e.co=d2.co AND e.cc2=d2.cc2
	LEFT OUTER JOIN CDept3 d3 ON e.co=d3.co AND e.cc3=d3.cc3
	LEFT OUTER JOIN CDept4 d4 ON e.co=d4.co AND e.cc4=d4.cc4
	LEFT OUTER JOIN CDept5 d5 ON e.co=d5.co AND e.cc5=d5.cc5

WHERE (e.empstatus='a' OR (e.empstatus='T' AND DATEDIFF(day,e.termdate,GETDATE()) < 30))
	
GO


