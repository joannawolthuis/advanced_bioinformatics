CREATE TABLE Mutations
(
  Chromosome int,
  Position float,
  ID varchar(255),
  Reference char,
  Alternate varchar(255),
  Quality float,
  Filter varchar(255),
  Format varchar(255
);


CREATE TABLE Samples
(
  Sample_ID varchar(255),
  Position varchar(255),
  GT varchar(255),
  AD float,
  DP int,
  GQ int,
  PGT varchar(255),
  PID varchar(255),
  PL bigint
 );
