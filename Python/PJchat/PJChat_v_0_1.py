#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as msgbox
from tkinter import colorchooser


class Message():
	"""
	Cette classe permet de gerer les messages
	Elle permet :
		- le cryptage/décryptage des messages
		- la lecture/ecriture de messages dans des fichiers
		- la gestion d'identité (nom d'utilisateur + id + mdp)
		- l'ajout d'utlisateuurs
		- la suppression d'utilisateurs
	"""

	def __init__(self):

		self.path = "/home/timothee/Documents/Documents/Programmation/Python/PJchat/"	# Chemin vers le dossier de la messagerie
		self.index = self.read_index() 						# Liste des utilisateurs (nom, id, mdp)
		self.user = ("Timothee", 1234, "coucou") 			# Utilidateur par default si pas de login (uniquement pour tests)
	
	def crypt(self, content):
		"""
		Cryptage d'un message
		:entrée: message à crypter (string)
		:sortie: message crypté (bytearray = liste de bytes)
		"""
		key=0b11011101 # Clé de cryptage

		# Décalage en ajoutant la valeur de la lettre precedante
		content_d=""
		for i in range(len(content)):
			if i == 0: 
				content_d += chr((ord(content[i])+62)%255)
				continue
			content_d += chr( ( ord(content[i])+ord(content[i-1])) %255)

		# Chaque caractère est mis dans le tableau en valeur ascii
		content_db = []
		for i in range(len(content_d)):
			content_db.append(ord(content_d[i]))

		# Chaque caratère du tableau est crypté par un xor de la clé
		content_dbx=[]

		for i in range(len(content_db)):
			content_dbx.append(content_db[i]^key)

		return bytearray(content_dbx)

	def decrypt(self, content_dbx):
		"""
		Décryptage d'un message (doit avoir été crypté avec la fonction crypt)
		:entrée: message crypté (bytearray = liste de bytes)
		:sortie: message décrypté (string)
		"""
		key=0b11011101 # Clé de décryptage

		# Chaque caractère est décrypté par un xor de la clé
		content_db=[]
		for i in range(len(content_dbx)):
			content_db.append(content_dbx[i]^key)

		# Les caractères sont joins
		content_d=""
		for i in range(len(content_db)):
			content_d += chr(content_db[i])

		# Re-décalage
		content=""
		for i in range(len(content_d)):
			if i == 0:
				if ord(content_d[i])-62 < 0:
					content += chr((ord(content_d[i])-62)%255)
				else:
					content += chr(ord(content_d[i])-62)
				continue

			if(ord(content_d[i])-ord(content[i-1]))>0:
				content += chr(ord(content_d[i])-ord(content[i-1]))
			else: 
				content += chr(ord(content_d[i])-ord(content[i-1])+255)
		return content

	def read_file(self, file):
		"""
		Lecture du contenu d'un fichier crypté
		:entrée: nom du fichier (string)
		:sortie: contenu du fichier décrypté (string)
		"""
		# Lecture du fichier
		try:
			with open(file, "rb") as f_crypted:
				return self.decrypt(f_crypted.read())

		# Si le fichier n'existe pas, retourne un message l'indiquant 
		except IOError:
			return "<1234>Désolé, vous n'avez aucun message...</>"
			
	def read_msg(self, idu):
		"""
		Lecture des messages adressées à un utilisateur (via l'id)
		:entrée: id de l'utilisateur (int)
		:sortie: messages reçus par l'utilisateur (liste de tuples (int, string))
		"""
		self.msg=[]
		f = self.read_file(self.id_to_filename(idu)) # Lecture du fichier
		if not f: return [("Nobody", "pas de message !")] # Si le fichier ne contient rien, afficher qu'il n'y a pas de message
		x = 0 # Nombre de caractères à passer
		j = 0 # Indique si on lit le contenu du message(1) ou non(0)
		id, text = 0, ""
		for i in range(len(f)):
			if x>0: # On avance de x caractère(s)
				x-=1
				continue
			if not j and f[i] == "<":
				id = int(f[i+1] + f[i+2] + f[i+3] + f[i+4]) # L'id correspond au nombre de 4 chiffres situé après un "<"
				x+=5 # On avance de 5 caractères car ils ont déjà été lu
				j=1  # On lit maintenant le contenu du message
				continue
			if j and f[i] == "<" and f[i+1] == "/" and f[i+2] == ">": # La balise "</>" indique la fin d'un message
				j=0 # On ne lit plus le contenu du message
				x=2 # On avance de 2 caratères
				self.msg.append((id, text))
				text =""
				continue
			if j:
				text+=f[i] # On ajoute le caractère si on lit le contenu du texte 
		return self.msg

	def send(self, id, content):
		"""
		Ecriture d'un message dans un fichier
		:entrées: l'id de l'utilisateur et le contenu du message (int, string)
		:sortie: Écriture dans le fichier (string)
		"""
		with open(self.id_to_filename(id), "ab") as f:
			f.write(self.write_format(content))

	def read_index(self):
		"""
		Lit le fichier d'index
		:entrée: None
		:sortie: liste de tuples (string, int, string)
		"""
		f = self.read_file(self.path + "index.txt") # Lecture du fichier index
		j= 0 # Indique si on lit le nom(0), l'id(1) ou le mdp(2)
		name, id , mdp = "", "", ""
		index = []
		for i in range(len(f)): # Lecture caractère par caractère
			if f[i] != "(": # On ne lit pas les "("
				if f[i] == ",":
					j+=1 
					continue
				if f[i] == ")":
					j=0
					index.append((name, int(id) , mdp))
					name, id , mdp = "", "", ""
					continue
				if j == 0:
					name += f[i]
				if j == 1:
					id += f[i]
				if j == 2:
					mdp += f[i]
		print("index=", index)
		return index

	def write_index(self, index=None):
		"""
		Ecriture du fichier index
		:entrée: index (liste de tuples (string, int, string))
		:sortie: Écriture dans le fichier index
		"""
		# Prend la valeur de l'index de l'objet si aucun n'est spécifié
		if index is None:
			index = self.index

		# Formatage
		index_ = ""
		for i in range(len(index)):
			index_ += "(" + str(index[i][0]) + "," + str(index[i][1]) + "," + str(index[i][2]) + ")"

		# Écriture
		with open(self.path + "index.txt", "wb") as f:
				f.write(self.crypt(index_))

	def get_index(self):
		"""
		Renvoie l'index
		:entrée: None
		:sortie: index (liste de tuples (string, int, string))
		"""
		return self.index

	def get_names(self):
		"""
		Renvoie la liste des noms de tous les utilisateurs
		:entrée: None
		:sortie: nom de tous les utilisateurs (liste of string)
		"""
		index = self.get_index()
		return [index[i][0] for i in range(len(index))]
		
	def get_name(self, id):
		"""
		Renvoie le nom de l'utilisateur correspondant à l'id
		:entrées: id (int)
		:sortie: nom correspondant à l'id (string)
		"""
		index = self.get_index()
		for i in range(len(index)):
			if index[i][1] == id:
				return index[i][0]

	def get_id(self, name):
		"""
		Renvoie l'id de l'utilisateur correspondant au nom
		:entrées: nom (string)
		:sortie: id correspondant au nom (int)
		"""
		index = self.get_index()
		for i in range(len(index)):
			if index[i][0] == name:
				return index[i][1]

	def id_to_filename(self, id):
		"""
		Renvoie le nom du fichier du correspondant à l'id
		:entrée: id (int)
		sortie: fichier correspondant à l'id (string)
		"""
		return self.path + "users/" + str(id) + ".txt"

	def write_format(self, content):
		"""
		Renvoie le string formaté pour l'écriture ("<0000>contenu du message</>")
		:entrée: message (string)
		:sortie: message formaté (string)
		"""
		return self.crypt("<" + str(self.user[1]).zfill(4) + ">" + content + "</>")

	def verif(self, name, mdp):
		"""
		Comparaison du nom et du mdp entrés 
		:entrées: nom et mdp (string, string)
		:sortie: True si correspondance, False si non (bool)
		"""
		for i in range(len(self.index)):
			if self.index[i][0] == name:
				if self.index[i][2] == mdp:
					self.user = self.index[i] # Définition de l'utilisateur 
					print("user = ", self.user)
					return True
		return False

	def add_user(self, name, mdp, id=int(0)):
		"""
		Ajoute un utlisateur
		:entrée: string, string, (int)
		:sortie: écriture dans fichier index
		"""
		
		# Vérifie que la syntaxe du nom est correcte
		for i in range(len(name)):
			if name[i] == "(" or name[i] == "," or name[i] == ")":
				return "Invalid name"

		# Vérifie que la syntaxe du mdp est correcte
		for i in range(len(mdp)):
			if mdp[i] == "(" or mdp[i] == "," or mdp[i] == ")":
				return "Invalid mdp"

		# Vérifie si le nom n'est pas déjà pris
		for i in range(len(self.index)):
			if self.index[i][0] == name:
				return "Invalid name used"

		# Vérifie que si l'id est déjà utilisé
		for i in range(len(self.index)):
			if id == self.index[i][1]:
				return "Invalid id used"

		# Vérifie si l'id est correct
		if (type(id) != int) or (id < 0):
			return "Invalid id"
		
		# Création d'un id si aucun n'est proposé
		idfound=0
		if id == 0: # Si l'id est 0 (s'il est non précisé)
			id=100 # On commence à 100 pour laisser la place à des numéros spéciaux 

			while 1:
				id +=1 # On incrémente 1

				# Cherche si l'id est déjà utlisé
				idfound=0
				for j in range(len(self.index)):
					if id == self.index[j][1]:
						idfound=1

				# Sorir de la boucle s'il n'est pas déjà utillisé		
				if not idfound:
					break

		# Ajout du nouvel utilisateur dans l'index contenu dans le programme
		self.index.append( (name, id, mdp) )

		self.write_index()

		# Ecrit un message de bienvenue au nouvel utilisateur
		self.send(id, "Bienvenue !")

	def del_user(self, name):
		"""
		Supprimme un utilisateur
		:entrée: nom de l'utilisateur (string)
		:sortie: suppression du fichier de messages de l'utilisateur et de son nom dans l'index
		"""
		for i in range(len(self.index)):
			if self.index[i][0] == name:
				os.remove("users/" + str(self.index[i][1]) + ".txt")	# Suppression du fichier de messages de l'utilisateur
				self.index.pop(i) # Suppression de son nom dans l'index
				self.write_index() # Réécriture de l'index actualisé
				return

	def del_msg(self, i):
		"""
		Supprime le message se trouvant à l'indice i du fichier des messages de l'utilisateur
		:entrée: index du message (int)
		:sortie: None
		"""
		self.msg.pop(i) # Suppression du message
		msg_=""
		for i in range(len(self.msg)):
			msg_ += "<" + str(self.msg[i][0]).zfill(4) + ">" + self.msg[i][1] + "</>" # Actualisation de la liste de messages

		with open(self.id_to_filename(self.user[1]), "wb") as f: # Réécriture des messages
			f.write(self.crypt(msg_))


class MainMsgApp(tk.Frame):
	"""
	Cette classe est le coeur de l'interface grafique
	C'est la fenetre principale dans laquel les messages reçus sont affichés
	"""

	def __init__(self, window, message):
		super().__init__(window)

		self.main_window = window 		# Fenetre Tk
		self.m = message 				# objet Message pour gerer les messages
		self.login_flag=0 				# Flag pour savaoir si le logi a été fait (utile lors de la supression des widgets du login)
		self.bg_color = "black"			# Couleur de l'arrière plan par défault
		self.text_color = "white"		# Couleur du texte par défault
		self.combostyle = ttk.Style()	# Objet Style pour la configuration des listes déroulantes

	def login(self):
		"""
		Affiche la fenetre qui permet de se connecter
		"""
		self.login_flag=1 # Flag permetant de masquer les widgets s'il y a eu un login (uilisation sans login limité aux tests)

		# Configuration de la fenêtre
		self.main_window.wm_attributes("-topmost", True)
		self.main_window.title("Identification")

		# Création des widgets
		self.name_label = tk.Label(self.main_window, text="Identifiant :")
		self.name_input = tk.Entry(self.main_window)
		
		self.mdp_label = tk.Label(self.main_window, text="Mot de passe :")
		self.mdp_input = tk.Entry(self.main_window)

		self.verif_button = tk.Button(self.main_window, text="Valider", command=lambda:self.verif_login())

		self.essaye_label = tk.Label(self.main_window, text="")

		# Affiche les widgets
		self.name_label.pack()
		self.name_input.pack()

		self.mdp_label.pack()
		self.mdp_input.pack()

		self.verif_button.pack()

	def verif_login(self):
		"""
		Affiche la page principale si l'identification est correcte
		Est appelée lorsque l'utilisateur appuit sur le bouton
		"""
		if m.verif(self.name_input.get(), self.mdp_input.get()):
			self.main()
		else:
			print("mdp incorrect")
			msgbox.showwarning(title="MDP INCORRECT", message="L'identifiant ou le mot de passe est incorrecte")
                                                
	def main(self):
		"""
		Affiche la page principale
		"""
		# Efface les widgets du login pour pouvoir en afficher d'autres après
		if self.login_flag:
			self.name_label.pack_forget()
			self.name_input.pack_forget()

			self.mdp_label.pack_forget()
			self.mdp_input.pack_forget()

			self.verif_button.pack_forget()

			self.login_flag = 0

		# Configuration de la fenêtre
		self.main_window.wm_attributes("-topmost", False)
		self.main_window.title("Messagerie 2.0 - " + str(self.m.user[0]))

		# Configuration du poids des lignes et colonnes lors du changement de taille de la fenêtre
		self.main_window.rowconfigure(0, weight=0)
		self.main_window.rowconfigure(1, weight=1)
		self.main_window.columnconfigure(0, weight=0)
		self.main_window.columnconfigure(1, weight=1)

		# Définition de la taille de la fenetre
		self.main_window.geometry("800x570")

		# Frame contenant les elements en haut de la page
		self.up_frame = tk.Frame(self.main_window, bg=self.bg_color)
		self.up_frame.grid(row=0, column=0, sticky="ew")
		self.up_frame.grid(columnspan=2)

		# Elements en haut de la page

		# Bouton d'actualisation des lessages
		self.refresh_button = tk.Button(self.up_frame, bg=self.bg_color, fg=self.text_color, text="Actualiser", command=self.refresh)
		self.refresh_button.grid(row=0, column=0)

		# Liste déroulante affichant les autres utilisateurs
		self.combostyle.configure('combostyle.TCombobox',
															selectbackground=self.bg_color, 
															fieldbackground=self.bg_color, 
															foreground=self.text_color, 
															background=self.text_color
															)
		self.corres_liste = ttk.Combobox(self.up_frame, values = "", style = 'combostyle.TCombobox')
		self.corres_liste.bind("<<ComboboxSelected>>", self.OnselectCorres)
		for name in self.m.get_names():
			if not name == self.m.user[0]:
				self.corres_liste['values'] = (*self.corres_liste['values'], name)
		self.corres_liste.grid(row=0, column=1)

		# Bouton ouvrant la fenre d'écriture d'unn message
		self.write_button = tk.Button(self.up_frame, bg=self.bg_color, fg=self.text_color, text="Ecrire", command=self.writeMsg)
		self.write_button.grid(row=0, column=2)

		# Bouton ouvrant la fenêtre de paramètres
		self.settings_button = tk.Button(self.up_frame, bg=self.bg_color, fg=self.text_color, text="Paramètres", command=self.settings)
		self.settings_button.grid(row=0, column=3)

		# Liste des messages
		self.msg_listbox = tk.Listbox(self.main_window, bg=self.bg_color, fg=self.text_color)

		# Lecture des messages
		self.refresh()

		# Création d'un évenement pour afficher le message quand on clique dessus et affichage de la liste
		self.msg_listbox.bind('<<ListboxSelect>>', self.print_msg)
		self.msg_listbox.bind("<Delete>", self.del_msg)
		self.msg_listbox.grid(row = 1, column=0, sticky="news")

		# Contenu du message
		self.msg_text = tk.Text(self.main_window, bg=self.bg_color, fg=self.text_color)
		self.msg_text.grid(row=1, column=1, sticky="nsew")

		self.msg_text.config(state="normal")
		self.msg_text.insert(tk.INSERT,"Pas de message")
		self.msg_text.config(state="disable")

		# Afficher les options réservées aux administrateurs (Timothée et Anthony)
		if m.user[0] == "Timothee" or m.user[0] == "Anthony":
			# Bouton d'ajout d'un utilisateur
			self.add_button = tk.Button(self.up_frame, bg=self.bg_color, fg=self.text_color, text="Add user", command=self.add_user)
			self.add_button.grid(row=0, column=4)

			# Bouton de suppression d'un utilisateur
			self.del_button = tk.Button(self.up_frame, bg=self.bg_color, fg=self.text_color, text="Del user", command=self.del_user)
			self.del_button.grid(row=0, column=5)

			# Bouton qui m'envoie un message contenant l'index
			self.index_button = tk.Button(self.up_frame, bg=self.bg_color, fg=self.text_color, text="Index", command=self.send_index)
			self.index_button.grid(row=0, column=6)

	def send_index(self):
		"""
		Envoie un message contenant l'index
		"""
		m.send(str(m.user[1]), str(m.get_index()))

	def add_user(self):
		"""
		Affiche la fenetre permetant d'ajouter un utilisateur
		"""
		add_w = tk.Toplevel() 
		add_interface = ModUserWindow(add_w, self.m)
		add_interface.add_user_w()

	def del_user(self):
		"""
		Affiche la fenetre permetant d'ajouter un utilisateur
		"""
		del_w = tk.Toplevel()
		del_interface = ModUserWindow(del_w, self.m)
		del_interface.del_user_w()

	def refresh(self):
		"""
		Met a jour la liste de messages
		:entrée: None
		:sortie: print (Affiche la liste de message actualisée)
		"""
		check=0
		# Lit les messages
		self.msgs = self.m.read_msg(m.user[1])

		#Supprime le contenu
		self.msg_listbox.delete(0,tk.END)

		# Si un correspodant est sélectionner, affiche les messages le concernant avec 20 caractères max
		for i in range(len(self.msgs)):
			if m.get_name(self.msgs[i][0]) == self.corres_liste.get():
				check=1
				msg_teaser = str(self.m.get_name(self.msgs[i][0])) + " " + str(self.msgs[i][1])
				if len(msg_teaser) > 20:
					 msg_teaser = msg_teaser[:20] + "..."
				self.msg_listbox.insert(0, msg_teaser)
		
		# Sinon Affiche tous les messages avec 20 caractères max
		if not check:
			for i in range(len(self.msgs)):
				msg_teaser = str(self.m.get_name(self.msgs[i][0])) + " " + str(self.msgs[i][1])
				if len(msg_teaser) > 20:
					 msg_teaser = msg_teaser[:20] + "..."
				self.msg_listbox.insert(0, msg_teaser)
		
	def print_msg(self, event):
		"""
		Affiche le message cliqué
		:entrée: event (quand un element de la liste est cliqué)
		:sortie: print (affiche le message)
		"""
		msg="" # message à afficher

		# Si un élément est selectioné uniquement
		if len(event.widget.curselection()):
			selection=event.widget.curselection() # index de l'élément

			# Si un correspondant est sélectionné, n'afficher que les messages le concernant
			if self.corres_liste.get():
				msgs_slcted = [self.msgs[i][1] for i in range(len(self.msgs)) if self.msgs[i][0] == m.get_id(self.corres_liste.get())]
				msg=msgs_slcted[self.msg_listbox.size()-selection[0]-1]
			else: # Sinon aficher tous les messages
				msg=self.msgs[self.msg_listbox.size()-selection[0]-1][1]

			# Supprimer l'ancien mesage et afficher le nouveau
			self.msg_text.config(state="normal")
			self.msg_text.delete(1.0, tk.END)
			self.msg_text.insert(tk.INSERT,msg)
			self.msg_text.config(state="disable")

	def OnselectCorres(self, event):
		"""
		Actualise la liste des messages lors du changemen de correspondant
		:entrée: event
		:sortie: None
		"""
		self.refresh()

	def writeMsg(self):
		"""
		Crée une fenetre pour ecrire le message
		"""
		w_window = tk.Toplevel()
		w_interface = WriteWindow(w_window, self.m)
		w_interface.print_w_window()

	def del_msg(self, event):
		"""
		Supprime un message
		:entrée: évènement de suppression (event)
		:sortir: None
		"""
		# Si un élément est selectioné uniquement
		if len(event.widget.curselection()):
			selection=event.widget.curselection() # index de l'élément
			# Supprime le message sélecionné si l'action est validée
			if "yes" == msgbox.askquestion("Attention", "Attention vous êtes sur le point de supprimer le message sélectionné\n Etes vous sur de vouloir poursuivre l'action ?"):
				m.del_msg(self.msg_listbox.size()-selection[0]-1)
				self.msg_listbox.delete(selection[0])

	def settings(self):
		"""
		Affiche la fenêtre de paramètres
		"""
		set_window = tk.Toplevel()
		set_interface = SettingsWindow(self.main_window, set_window, self.m)
		set_interface.print_set_window()

	def set_background_color(self, color):
		"""
		Modifie la couleur d'arrière plan et actualisation de la page principale
		:entrée: couleur (string)
		:sortie: None
		"""
		self.bg_color = color
		self.main()

	def get_background_color(self):
		"""
		Renvoie la couleur de l'arrière plan
		"""
		return self.bg_color

	def set_text_color(self, color):
		"""
		Modifie la couleur du texte et actualisation de la page principale
		:entrée: couleur (string)
		:sortie: None
		"""
		self.text_color = color
		self.main()

	def get_text_color(self):
		"""
		Renvoie la couleur du texte
		"""
		return self.text_color


class WriteWindow(tk.Frame):
	"""
	Cette classe gere l'écriture des messages
	Elle permet à l'utilisateur de les ecire puis les envoyer
	"""

	def __init__(self, w_window, message):
		super().__init__(window)
		self.w_window = w_window 	# Fenetre Tk 
		self.nb_corres=0 					# Nombre de correspondants
		self.corres_liste=[] 		 	# Liste des Combobox(menu déroulant) des correspondants
		self.one_corres_frame=[] 	# Liste des frame contenant les widgets servant a choisir un correspondant

	def print_w_window(self):
		"""
		Cette fonction permet d'afficher les widgets de la fenetre
		"""

		# Initialisation de la fenetre
		self.w_window.geometry("300x300")
		self.w_window.title("Ecrire - Messagerie 2.0")
		self.w_window.configure(bg=interface.get_background_color())

		# Configuration du poids des lignes et colonnes lors du changement de taille de la fenetre
		self.w_window.rowconfigure(0, weight=0)
		self.w_window.rowconfigure(1, weight=1)
		self.w_window.columnconfigure(0, weight=1)


		# Création de la frame scrollable contenant les destinataires
		canvas = tk.Canvas(self.w_window, bd=0, bg=interface.get_background_color())
		container = tk.Frame(self.w_window, bg=interface.get_background_color())
		canvas = tk.Canvas(container, height=100, bg=interface.get_background_color())
		scrollbar = tk.Scrollbar(container, bg=interface.get_background_color(), orient="vertical", command=canvas.yview)
		self.corres_frame = tk.Frame(canvas, bg=interface.get_background_color())

		self.corres_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

		canvas.create_window((0, 0), window=self.corres_frame, anchor="nw")

		canvas.configure(yscrollcommand=scrollbar.set)

		container.grid(row=0, column=0)
		canvas.grid(row=0, column=0, sticky="nsew")
		scrollbar.grid(row=0, column=1, sticky="nsw")

		# Bouton permettant d'ajouter ou enlever des destinataires
		self.add_button = tk.Button(self.corres_frame, text="+", command=self.add_corres, bg=interface.get_background_color(), fg=interface.get_text_color())
		self.del_corres_button = tk.Button(self.corres_frame, text="-", command=self.del_corres, bg=interface.get_background_color(), fg=interface.get_text_color())

		# Ajout du premier destinataire
		self.add_corres()

		# Création d'un widget Text permettant à l'utilisateur d'écrire le message
		self.msg_text = tk.Text(self.w_window, bg=interface.get_background_color(), fg=interface.get_text_color())
		self.msg_text.grid(row=1, column=0, sticky="nsew")

		# Bouton d'envoi
		self.send_button = tk.Button(self.w_window, bg=interface.get_background_color(), fg=interface.get_text_color(), text="envoyer", command=self.send)
		self.send_button.grid(sticky="se")

	def send(self):
		"""
		Cette fonction envoit le message ecrit à/aux correspondants choisis
		"""

		# Récupération des correspondants
		corres=[]
		for i in range(len(self.corres_liste)):
			cor=self.corres_liste[i].get()
			if cor in m.get_names():
				corres.append(cor)

		# Message d'erreur s'il n'y a pas de destinataire choisi
		if not(len(corres)):
			msgbox.showerror(title="Destinataire ???", message="Veuillez sélectionner un destinataire")
			return

		# Récupère le message
		msg=self.msg_text.get("1.0", tk.END)
		msg=msg[:len(msg)-1]

		# Message d'erreur s'il n'y a pas de message écrit
		if not(len(msg)):
			msgbox.showerror(title="Message vide", message="Veuillez écrire un message avant l'envoie")
			return

		# Message d'erreur si le message est trop long (plus de 100'000 caractères)
		if len(msg) > 100000:
			msgbox.showerror(title="Taille message", message="Le message ne peut pas dépasser 100'000 caractères")
			return

		# Message d'erreur si le message contient "</>" car c'est une balise
		for i in range(len(msg)-2):
			if msg[i:i+2] == "</>":
				msgbox.showerror(title="Invalid syntax", message="Le message ne peut contenir l'association de caractères : \"</>\"\nVeuillez le corriger avan l'envoie")
				return

		# Envoi à tous les correspondants
		for cors in corres:
			m.send(m.get_id(cors), msg)
		self.msg_text.delete("1.0", tk.END)
		self.w_window.destroy()

	def add_corres(self):
		"""
		Ajoute une ligne permetant de choisir un correspondant suplémentaire
		"""

		# Incrémentation du nombre de destinataire
		self.nb_corres +=1

		# Création d'une nouvelle frame contenant le label et la liste permetant de choisir le destinataire
		self.one_corres_frame.append(tk.Frame(self.corres_frame))
		self.one_corres_frame[self.nb_corres-1].grid()

		# Création et affichage du label
		to_label = tk.Label(self.one_corres_frame[self.nb_corres-1], text="To : ", bg=interface.get_background_color(), fg=interface.get_text_color())
		to_label.grid(row=0, column=0)

		# Créaion de la liste permetant de choisir le destinataire
		self.corres_liste.append(ttk.Combobox(self.one_corres_frame[self.nb_corres-1], values = "", style = 'combostyle.TCombobox')) #
		for name in m.get_names():
			if not name == m.user[0]:
				self.corres_liste[self.nb_corres-1]['values'] = (*self.corres_liste[self.nb_corres-1]['values'], name)
		self.corres_liste[self.nb_corres-1].grid(row=0, column=1)

		# Replace le bouton de suppression de destinataire
		if len(self.one_corres_frame) > 1:
			self.del_corres_button.grid(row=len(self.one_corres_frame), column=1)
		else:
			self.del_corres_button.grid_forget() # Le cacher s'il ne reste qu'un destinataire

		# Replace le bouton d'ajout de destinataire
		if len(m.get_names()) - len(self.one_corres_frame)-1 > 0:
			self.add_button.grid(row=len(self.one_corres_frame), column=2)
		else:
			self.add_button.grid_forget() # Le cacher s'il y a autant de destinataire que d'utilisateurs de la messagerie

	def del_corres(self):
		"""
		Supprime le dernier destinataire
		"""

		# Efface et supprime le Combobox de la dernière frame
		self.corres_liste[len(self.corres_liste)-1].destroy()
		self.corres_liste = self.corres_liste[:-1]

		# Efface et supprime la dernière frame
		self.one_corres_frame[len(self.one_corres_frame)-1].destroy()
		self.one_corres_frame = self.one_corres_frame[:-1]

		# Replace les boutons
		self.del_corres_button.grid(row=len(self.one_corres_frame), column=1)
		self.add_button.grid(row=len(self.one_corres_frame), column=2)

		# Enleve 1 au compteur de destinataires
		self.nb_corres -=1


class ModUserWindow(tk.Frame):
	"""
	Cette classe permet de gerer le fenetre d'ajout d'un utilisateur
	"""

	def __init__(self, mod_u_window, message):
		super().__init__(window)
		self.m = message # objet Message pour gerer les messages
		self.mod_u_window = mod_u_window # Fenetre Tk
		
	def add_user_w(self):
		"""
		Affiche la fenetre qui permet d'ajouter un utilisateur'
		"""
		self.login_flag=1
		self.mod_u_window.wm_attributes("-topmost", True)
		self.mod_u_window.title("Ajouter un utlisateur")
		self.mod_u_window.configure(bg=interface.get_background_color())

		# Création des widgets
		self.name_label = tk.Label(self.mod_u_window, text="Identifiant :", bg=interface.get_background_color(), fg=interface.get_text_color())
		self.name_input = tk.Entry(self.mod_u_window, bg=interface.get_background_color(), fg=interface.get_text_color())
		
		self.mdp_label = tk.Label(self.mod_u_window, text="Mot de passe :", bg=interface.get_background_color(), fg=interface.get_text_color())
		self.mdp_input = tk.Entry(self.mod_u_window, bg=interface.get_background_color(), fg=interface.get_text_color())

		self.id_label = tk.Label(self.mod_u_window, text="ID : (optionel)", bg=interface.get_background_color(), fg=interface.get_text_color())
		self.id_input = tk.Entry(self.mod_u_window, bg=interface.get_background_color(), fg=interface.get_text_color())

		self.button = tk.Button(self.mod_u_window, text="Valider", command=lambda:self.add_user(), bg=interface.get_background_color(), fg=interface.get_text_color())

		# Affiche les widgets
		self.name_label.grid()
		self.name_input.grid()

		self.mdp_label.grid()
		self.mdp_input.grid()

		self.id_label.grid()
		self.id_input.grid()

		self.button.grid()

	def add_user(self):
		"""
		Ajoute un utilisateur quand le bouton est appuyé
		"""

		# Récupération du nom, mdp et id
		name = self.name_input.get()
		mdp = self.mdp_input.get()
		id = self.id_input.get()

		# Vérifie que l'utilisaeur a rentré un utilisateur et un mot de passe
		if not len(name):
			msgbox.showerror(title="Invalid name", message="Veuillez entrer un nom")
			return
		if not len(mdp):
			msgbox.showerror(title="Invalid mdp", message="Veuillez entrer un mdp")
			return

		if len(id):
			try:
				id=int(id) # convertion de l'id en int
			except:
				id = "a" # Sinon convertion en caractère pour lever une erreur

			error_add=self.m.add_user(name, mdp, id) # Ajout d'un utilisateur avec id s'il y en a un
		else:
			error_add=self.m.add_user(name, mdp) # Sinon ajout d'un utilisateur sans id précis

		# vérifie que la syntaxe du nom et et mdp soient correctes
		if error_add == "Invalid name":				msgbox.showerror(title="Invalid name", message="Le nom ne peut contenir les caractères \"(\", \",\" ou \")\" ")
		if error_add == "Invalid mdp":				msgbox.showerror(title="Invalid mdp", message="Le mot de passe ne peut contenir les caractères \"(\", \",\" ou \")\" ")
		if error_add == "Invalid name used":	msgbox.showerror(title="Invalid name", message="Ce nom est déja utilisé")
		if error_add == "Invalid id used":		msgbox.showerror(title="Invalid id", message="Cet id est déja utilisé")
		if error_add == "Invalid id":					msgbox.showerror(title="Invalid id", message="L'id doit être un nombre supérieur à 0")
		

		# Fermeture de la fenêtre s'il n'y a pas d'erreur
		if not error_add:
			self.mod_u_window.destroy()

	def del_user_w(self):
		"""
		Affiche la fenetre qui permet de supprimer un utilisateur'
		"""
		#Configuration de la fenêtre
		self.mod_u_window.title("Supprimer un utlisateur")
		self.mod_u_window.configure(bg=interface.get_background_color())

		#	Affiche le label contenant l'instruction
		self.label = tk.Label(self.mod_u_window, text="Choisissez un utilisateur à supprimer", bg=interface.get_background_color(), fg=interface.get_text_color())
		self.label.grid(row=0, column=0)

		# Affiche la liste des utlisateurs
		self.corres_liste = ttk.Combobox(self.mod_u_window, values = "", style = 'combostyle.TCombobox')
	
		for name in m.get_names():
			if not name == m.user[0]:
				self.corres_liste['values'] = (*self.corres_liste['values'], name)
		self.corres_liste.grid(row=1, column=0)

		# Affiche le bouton de validation
		self.button = tk.Button(self.mod_u_window, bg=interface.get_background_color(), fg=interface.get_text_color(), text="Valider", command=lambda:self.del_user())
		self.button.grid(row=3, column=0)

	def del_user(self):
		"""
		Supprime un utilisateur quand le bouton est appuyé
		"""
		# Supprime l'utilisateur sélecionné si l'action est validée
		if "yes" == msgbox.askquestion("Attention", "Attention vous êtes sur le point de supprimer l'utilisateur sélectionné\n Etes vous sur de vouloir poursuivre l'action ?"):
			m.del_user(self.corres_liste.get())

			self.mod_u_window.destroy()	# Fermeture de la fenêtre


class SettingsWindow(tk.Frame):
	"""
	Permet de modifier des paramètres :
		- couleurs
	"""

	def __init__(self, main_window, set_window, m):
		super().__init__(window)
		self.set_window = set_window # Fenetre Tk

	def print_set_window(self):
		"""
		Cette fonction permet d'afficher les widgets de la fenetre
		"""
		# Configuration de la fenêtre
		self.set_window.title("Paramètres")
		self.set_window.configure(bg=interface.get_background_color())

		# Bouton pour changer la couleur de l'arrière plan
		bg_color_button = tk.Button(self.set_window, bg=interface.get_background_color(), fg=interface.get_text_color(), text="changer la couleur de l'arrière plan", command=lambda:self.choose_bg_color())
		bg_color_button.grid(row=0, column=0, sticky="nsew")

		# Bouton pour changer la couleur du texte
		text_color_button = tk.Button(self.set_window, bg=interface.get_background_color(), fg=interface.get_text_color(), text="changer la couleur du texte", command=lambda:self.choose_text_color())
		text_color_button.grid(row=1, column=0, sticky="nsew")

	def choose_bg_color(self):
		"""
		Permet de changer la couleur de l'arrière plan
		"""
		color = colorchooser.askcolor(title ="Couleur de l'arrière plan")[1]
		if color:
			interface.set_background_color(color)

		self.set_window.destroy() # Fermeture de la fenêtre

	def choose_text_color(self):
		color = colorchooser.askcolor(title ="Couleur de l'arrière plan")[1]
		if color:
			interface.set_text_color(color)

		self.set_window.destroy() # Fermeture de la fenêtre


if __name__ == "__main__":
	m = Message()
	window = tk.Tk()
	interface = MainMsgApp(window, m)
	interface.login()
	window.mainloop()

"""
	print(m.decrypt(m.crypt("coucou !")))
	print("index = ", m.get_index())
	print("names = ", m.get_names())
	print("1234's name = ", m.get_name(1234))
	print("Anthony's id = ", m.get_id("Anthony"))
	m.send(5896, "ca te dit on se fait une petanque ?")
	print("msg 5896=", m.read_msg(5896))
	print(m.verif("Anthony", "6969"))
"""
"""
print("index = ", m.get_index())
m.add_user("User02", "2")
print("index = ", m.get_index())
m.add_user("User01", "1")
"""
"""
print("index = ", m.get_index())
m.del_user("User03")
print("index = ", m.get_index())
"""
"""
with open("index.txt", "wb") as f:
	#f.write(m.crypt("(Timothee,1234,coucou)(Anthony,6969,6969)(default, 642, default)(User1, 1, 1)(User2, 2, 2)"))
	#f.write(m.crypt("(Anthony,6969,6969)(default, 642, default)(User1, 1, 1)(User2, 2, 2)"))
	f.write(m.crypt("(Timothee,1234,coucou)(Anthony,6969,6969)"))
"""