class Assignment:
	def __init__(self, d, score, total):
		self._description = d
		self._score = score
		self._total = total

	def getDescription(self)->str:
		return self._description

	def getScore(self)->float:
		return self._score

	def getTotal(self)->float:
		return self._total

	def changeScore(self, score:float):
		self._score = score

class CategoryAssignment(Assignment):
	def __init__(self, d, cat, score, total):
		super().__init__(d, score, total)
		self._category = cat

	def getCategory(self)->str:
		return self._category

class Student:
	def __init__(self, id):
		self._ID = id
		self._assignments = []

	def getId(self)->int:
		return self._ID

	def getScore(self, assignmentName:str)->float:
		for a in self._assignments:
			if a.getDescription() == assignmentName:
				return a.getScore()

	def getScores(self)->list:
		return self._assignments

	def addAssignment(self, score:Assignment):
		self._assignments.append(score)

	def changeScore(self, assignmentName: str, score: float):
		for a in self._assignments:
			if a.getDescription() == assignmentName:
				a.changeScore(score)
				break

	def removeScore(self, assignmentName: str):
		for a in self._assignments:
			if a.getDescription() == assignmentName:
				self._assignments.remove(a)
				break

class Gradebook:
	def __init__(self):
		self._student = []

	def addStudent(self, student: Student):
		num = 0
		for i in self._student:
			newId = i.getId()
			stud = student.getId()
			if newId == stud:
				num = 1
		if num == 0:
			self._student.append(student)

	def dropStudent(self, id: int):
		for i in self._student:
			newId = i.getId()
			if newId == id:
				self._student.remove(i)

	def search(self, id:int)->Student:
		for i in self._student:
			newId = i.getId()
			if newId == id:
				return i

	def addAssignment(self, id:int, score:Assignment):
		for i in self._student:
			newId = i.getId()
			if newId == id:
				i.removeScore(score)
				i.addAssignment(score)

class TotalPointsGradebook(Gradebook):
	def __init__(self):
		super().__init__()

	def writeGradebookRecord(self, id: int, fileName: str):
		outfile = open(fileName, "w")
		if self.search(id) != None:
			stud = self.search(id)
			studList = stud.getScores()
			outfile.write("%d\n" % id)
			score = 0
			total = 0
			per = 0
			for i in studList:
				outfile.write("%s\n" % i.getDescription())
				outfile.write("%d/%d\n" % (i.getScore(), i.getTotal()))
				score = score + i.getScore()
				total = total + i.getTotal()
			per = (score/total) * 100
			outfile.write("Total: %d/%d\n" % (score, total))
			outfile.write("Percentage: %f" % per)
		else:
			outfile.write("Student Not Found")
		outfile.close()

	def classAverage(self)->float:
		num = len(self._student)
		totalStuds = 0
		for i in self._student:
			studList = i.getScores()
			score = 0
			total = 0
			per = 0
			for j in studList:
				score = score + j.getScore()
				total = total + j.getTotal()
			per = score/total
			totalStuds = totalStuds + per
		return totalStuds/num*100

class CategoryGradebook(Gradebook):
	def __init__(self):
		super().__init__()
		self._collection = []

	def addCategory(self, description:str, weight:float):
		self._collection.append((description, weight))

	def isBalanced(self)->bool:
		total = 0
		for i in self._collection:
			total = total + i[1]
		if total == 100:
			return True
		return False

	def writeGradebookRecord(self, id: int, fileName: str):
		outfile = open(fileName, "w")
		if self.search(id) != None:
			stud = self.search(id)
			studList = stud.getScores()
			outfile.write("%d\n" % id)
			pers = []
			for j in self._collection:
				score = 0
				total = 0
				for i in studList:
					cat = i.getCategory()
					if cat == j[0]:
						outfile.write("%s: " % cat)
						outfile.write("%s\n" % i.getDescription())
						outfile.write("%d/%d\n" % (i.getScore(), i.getTotal()))
						score = score + i.getScore()
						total = total + i.getTotal()
				pers.append(score/total)

			per = 0
			n = 0
			for k in self._collection:
				outfile.write("%s: %f\n" % (k[0], pers[n]*100))
				per = per + (pers[n]*k[1])
				n = n + 1
			per = per*100
			outfile.write("Percentage: %f" % per)
		else:
			outfile.write("Student Not Found")
		outfile.close()

	def classAverage(self)->float:
		num = len(self._student)
		totalStuds = 0
		for l in self._student:
			studList = l.getScores()
			pers = []
			for j in self._collection:
				score = 0
				total = 0
				for i in studList:
					cat = i.getCategory()
					if cat == j[0]:
						score = score + i.getScore()
						total = total + i.getTotal()
				pers.append(score/total)
			per = 0
			n = 0
			for k in self._collection:
				per = per + (pers[n]*k[1])
				n = n + 1
			totalStuds = totalStuds + per
		return totalStuds/num