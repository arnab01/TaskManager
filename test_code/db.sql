-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Master`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Master` (
  `Role_id` INT NOT NULL,
  `Role_Name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Role_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `User_id` INT NOT NULL AUTO_INCREMENT,
  `User_Name` VARCHAR(45) NOT NULL,
  `First_Name` VARCHAR(45) NOT NULL,
  `Last_Name` VARCHAR(45) NULL,
  `User_Email` VARCHAR(45) NOT NULL,
  `Role_id` INT NOT NULL,
  `Phone_No` INT NOT NULL,
  PRIMARY KEY (`User_id`),
  INDEX `Role_id_idx` (`Role_id` ASC) VISIBLE,
  UNIQUE INDEX `User_Name_UNIQUE` (`User_Name` ASC) VISIBLE,
  CONSTRAINT `Role_id`
    FOREIGN KEY (`Role_id`)
    REFERENCES `mydb`.`Master` (`Role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Teams`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Teams` (
  `Team_id` INT NOT NULL,
  `Team_Name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Team_id`),
  UNIQUE INDEX `Team_Name_UNIQUE` (`Team_Name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`User_Team_Mapping`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User_Team_Mapping` (
  `User_id` INT NOT NULL,
  `Team_id` INT NOT NULL,
  INDEX `User_id_idx` (`User_id` ASC) VISIBLE,
  INDEX `Team_id_idx` (`Team_id` ASC) VISIBLE,
  CONSTRAINT `User_id`
    FOREIGN KEY (`User_id`)
    REFERENCES `mydb`.`User` (`User_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Team_id`
    FOREIGN KEY (`Team_id`)
    REFERENCES `mydb`.`Teams` (`Team_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tasks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Tasks` (
  `Task_id` INT NOT NULL,
  `Title` VARCHAR(45) NOT NULL,
  `Description` VARCHAR(1000) NULL,
  `Priority` VARCHAR(20) NOT NULL,
  `Planned_Date` DATE NOT NULL,
  `Assignee` VARCHAR(45) NOT NULL,
  `Reporter` VARCHAR(45) NOT NULL,
  `Status` VARCHAR(45) NOT NULL,
  `Team_Name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Task_id`),
  INDEX `Assignee_idx` (`Assignee` ASC) VISIBLE,
  INDEX `Reporter_idx` (`Reporter` ASC) VISIBLE,
  INDEX `Team_Name_idx` (`Team_Name` ASC) VISIBLE,
  CONSTRAINT `Assignee`
    FOREIGN KEY (`Assignee`)
    REFERENCES `mydb`.`User` (`User_Name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Reporter`
    FOREIGN KEY (`Reporter`)
    REFERENCES `mydb`.`User` (`User_Name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Team_Name`
    FOREIGN KEY (`Team_Name`)
    REFERENCES `mydb`.`Teams` (`Team_Name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
