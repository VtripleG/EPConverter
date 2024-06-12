CREATE TABLE IF NOT EXISTS "disciplines" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"code" NUMERIC NOT NULL,
	"educational_program_id" INTEGER NOT NULL,
	"name" TEXT,
	"department_code" INTEGER,
	UNIQUE ("code", "educational_program_id"),
	FOREIGN KEY("educational_program_id") REFERENCES "educational_programs"("id")
);
CREATE TABLE IF NOT EXISTS "educational_programs" (
	"id" INTEGER NOT NULL UNIQUE,
	"direction_code" TEXT NOT NULL,
	"direction_name" TEXT NOT NULL,
	"profile" TEXT NOT NULL,
	"start_year" INTEGER,
	"education_form" TEXT,
	UNIQUE ("direction_code", "start_year", "education_form"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "competencies_list" (
	"id" INTEGER NOT NULL UNIQUE,
	"discipline_id" INTEGER NOT NULL,
	"competence_guide_id" INTEGER NOT NULL,
	"know" TEXT,
	"can" TEXT,
	"master" TEXT,
	FOREIGN KEY("competence_guide_id") REFERENCES "competencies_guide"("id"),
	FOREIGN KEY("discipline_id") REFERENCES "disciplines"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "laboriousness" (
	"id" INTEGER NOT NULL UNIQUE,
	"descipline_id" INTEGER NOT NULL,
	"semester_number" INTEGER NOT NULL,
	"work_type" TEXT,
	"hours_number" INTEGER,
	UNIQUE (
		"descipline_id",
		"semester_number",
		"work_type"
	),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("descipline_id") REFERENCES "disciplines"("id")
);
CREATE TABLE IF NOT EXISTS "competencies_guide" (
	"id" INTEGER NOT NULL UNIQUE,
	"competence_code" TEXT NOT NULL,
	"educational_program_id" INTEGER NOT NULL,
	"content" TEXT,
	"code" INTEGER NOT NULL,
	UNIQUE(
		"competence_code",
		"educational_program_id"
	) PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("educational_program_id") REFERENCES "educational_programs"("id")
);