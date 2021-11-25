import unittest2 as unittest
import app

class TestApp(unittest.TestCase):

	def __init__(self,*args, **kwargs):
		super(TestApp, self).__init__(*args, **kwargs)
		self.client = app.app.test_client()

	def test_script(self):
		self.assertEqual(app.script("sample.txt"), "sample.csv")
	
	def test_generate_texts_from_txt(self):
		self.assertEqual(app.generate_texts_from_txt("sample.txt"), ["Es war einmal in Deutschland ein kleiner, lieblicher und sanfter Trollmann. Sein Name war Gerold. \"Du bist mein Lieblingsbaum\" sagte er oft zu seinem Baum.\n\"Warum stehst du einsam und alleine in der Garten\"? fragte <B>sein Baum</> jedesmal wenn Gerold vorbeikam. \"Wenn du bei mir bist, geht die Welt nicht unter\" sagte Gerold und blieb stehen. \"Du bist mein Gefährte, mein Beschützer, mein Freund. Und ich werde nie alleine sein.\"\n\"Aber ich bin nie alleine\", sagte der Baum. (S16/FEB.00260 Der Spiegel, [Wochenzeitschrift], 20.02.2016, S. 86. - Sachgebiet: Wirtschaft, Originalressort: Wirtschaft; Brandbrief an die Piloten)", 
		"\"Dann komm mich besuchen\", säuselte der Trollmann. \"Nein\", antwortete der Baum, \"Ich kann nicht für immer mit dir gehen. Du bist ein Mensch, Gerold, und wirst immer wieder weggehen. Das ist das Schlimme daran. Du gehst, ich bleibe. Gerold, wenn dennoch einmal der Tag kommt, an dem du für immer bei mir bleiben willst, dann brauchst du dir nichts einzubilden. Bleib bei mir bis in alle Ewigkeit.\" \nGerold antwortete: \"Nein, das werde ich nicht tun. Einmal wird meine Frau da sein und dann wirst du mir nicht mehr nahe sein.\"\n (S66/AUG.00270 Der Spiegel, [Wochenzeitschrift], 22.08.1966, S. 108. - Sachgebiet: Sport, Originalressort: Sport; Tod am 17. Grün)",''])

#create functions to test the flask api as well:
	def test_home(self):
		client = app.app.test_client()
		result = client.get('/')
		self.assertEqual(result.status_code, 200)

#test endpoint "/"
	def test_home_fail(self):
		response = self.client.get('/home')
		self.assertNotEqual(response.status_code, 200)
#test endpoint "/data"
	def test_data(self):
		response = self.client.get('/data')
		self.assertEqual(response.status_code, 200)
	def test_data_fail(self):
		response = self.client.get('/data1')
		self.assertNotEqual(response.status_code, 200)
#test endpoint "/download"
	def test_download(self):
		response = self.client.get('/download')
		self.assertEqual(response.status_code, 302)
	def test_download_fail(self):
		response = self.client.get('/download1')
		self.assertNotEqual(response.status_code, 200)
#test endpoint "/download/<filename>"
	def test_download_file(self):
		response = self.client.get('/download/sample.csv')
		self.assertEqual(response.status_code, 200)
	def test_download_file_fail(self):
		response = self.client.get('/download1/test_file.txt')
		self.assertNotEqual(response.status_code, 200)

if __name__ == '__main__':
	unittest.main()