/*
  Warnings:

  - You are about to drop the column `clerkid` on the `User` table. All the data in the column will be lost.

*/
-- DropIndex
DROP INDEX "User_clerkid_key";

-- AlterTable
ALTER TABLE "User" DROP COLUMN "clerkid";
