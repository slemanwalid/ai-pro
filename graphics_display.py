import tkinter as  tk
import tkinter.messagebox
import weakref


class Board:

    def __init__(self, master):
        super().__init__()
        master.title("Four in a row")
        self.__play_again = False
        self.__canvas = tk.Canvas(master, width=700, height=600)
        self.__label = tk.Label(master)
        self.__board_image = tk.PhotoImage(file='./Board_image.png')
        self.__canvas.create_image(0, 0, anchor=tk.NW, image=self.__board_image)
        # self.__button = master.bind("<Button-1>", self._left_click_handler)

        # self.build_buttons()
        self.__label.pack()
        self.__canvas.pack()
    def reset(self):
        self.__canvas.destroy()
        self.__canvas = tk.Canvas(self, width=700, height=600)
        self.__board_image = tk.PhotoImage(file='./Board_image.png')
        self.__canvas.create_image(0, 0, anchor=tk.NW, image=self.__board_image)
        # self.__button = self.bind("<Button-1>", self._left_click_handler)
        self.__canvas.pack()
    # def _left_click_handler(self, coord):
    #     col = coord.x// 100
    #     valid_move, row = self.__game.make_move(col)
    #     if not valid_move:
    #         tkinter.messagebox.showinfo('Column is full', 'Try another one')
    #         return
    #     self.draw_ball((row, col))
    #     if self.__game.is_over():
    #         winner = self.__game.get_winner()
    #         if winner == 0:
    #             tkinter.messagebox.showinfo('Game over', 'Board is full')
    #             self.play_again_or_quit()
    #             return True
    #
    #         elif winner == 1 or winner == 2:
    #             self.specify_winner_balls()
    #             tkinter.messagebox.showinfo('Game over', 'Player with ' + self.BALLS[winner] + ' ball has won')
    #             self.play_again_or_quit()
    #             return True

    def draw_ball(self, row, col, player):
        if player in self.BALLS.keys():
            self.__canvas.create_oval(15 + 100 * col, 15 + 100 * row, 97 + 100 * col, 97 + 100 * row,
                                      fill=self.BALLS[player])

    # def specify_winner_balls(self):
    #     """
    #     This function causing the discs which achieved the victory in the player game to be distinctive
    #     """
    #     cor = self.__game.winner_coordinates()
    #     for i in range(4):
    #         self.__canvas.create_oval(15 + 100 * (cor[0][1] + i * cor[1][1]), 15 + 100 * (cor[0][0] + i * cor[1][0]),
    #                                   97 + 100 * (cor[0][1] + i * cor[1][1]), 97 + 100 * (cor[0][0] + i * cor[1][0]),
    #                                   width=5)

    # def update_state(self, state, action, opponent_action):
    #     # if action == Action.LEFT:
    #     #     self.grid.move_tiles_left()
    #     # elif action == Action.RIGHT:
    #     #     self.grid.move_tiles_right()
    #     # elif action == Action.UP:
    #     #     self.grid.move_tiles_up()
    #     # elif action == Action.DOWN:
    #     #     self.grid.move_tiles_down()
    #     # elif action is Action.STOP:
    #     #     pass
    #     # else:
    #     #     raise Exception("Got unknown action.")
    #     self.draw_ball(opponent_action.row, opponent_action.column, opponent_action.value)
    #     self.mainloop_iteration()




class GabrieleCirulli2048GraphicsDisplay(tk.Tk):
    r"""
    Gabriele Cirulli's 2048 puzzle game;

    Python3-Tkinter port by Raphaël Seban;
    """
    BALLS = {1: 'red', 2: 'yellow'}

    def __init__(self, new_game_callback, quit_game_callback, human_agent):
        super(GabrieleCirulli2048GraphicsDisplay, self).__init__()
        self._new_game_callback = new_game_callback
        self._quit_game_callback = quit_game_callback
        self._padding = 10
        self.game_state = None
        self._mouse_click_observers = []
        self._build_ui(human_agent)
        self._board = None

    def _build_ui(self, human_agent):
        self.title("Intro to AI -- EX2")
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.resizable(width=False, height=False)
        self.__canvas = tk.Canvas(self, width=700, height=600)
        self.__label = tk.Label(self)
        self.__board_image = tk.PhotoImage(file='./Board_image.png')
        self.__canvas.create_image(0, 0, anchor=tk.NW, image=self.__board_image)
        self.__label.pack()
        self.__canvas.pack()
        # look'n'feel
        # ttk.Style().configure(".", font="sans 10")
        # get 2048's grid
        # self.grid = GG.Game2048Grid(self, tile_animation=human_agent)
        # if human_agent:
        #     self.hint = ttk.Label(
        #         self, text="Hint: use keyboard arrows to move tiles."
        #     )
        # else:
        #     self.hint = ttk.Label(
        #         self, text=""
        #     )
        # self.score = GameScore(self)
        # self.hiscore = GameScore(self, label="Highest:")
        # self.grid.pack(side=TK.TOP, padx=self._padding, pady=self._padding)
        # self.hint.pack(side=TK.TOP)
        # self.score.pack(side=TK.LEFT)
        # self.hiscore.pack(side=TK.LEFT)
        # if human_agent:
        #     tk.Button(self, text="Ciao!", command=self.quit_app).pack(side=tk.RIGHT, padx=self._padding,
        #                                                                pady=self._padding)
        #     tk.Button(self, text="New Game", command=self._new_game_callback).pack(side=tk.RIGHT)
        # else:
        #     tk.Button(self, text="Ciao!", command=self.quit_app, state=tk.DISABLED).pack(side=tk.RIGHT,
        #                                                                                   padx=self._padding,
        #                                                                                   pady=self._padding)
        #     tk.Button(self, text="New Game", command=self._new_game_callback, state=tk.DISABLED).pack(side=tk.RIGHT)

    def _left_click_listener(self, event):
        """Handle mouse left-click events and notify observers."""
        # Notify all observers about the mouse click
        print(event)
        for observable in self._mouse_click_observers:

            observable()(event)
    def draw_ball(self, row, col, player):
        if player in self.BALLS.keys():
            self.__canvas.create_oval(15 + 100 * col, 15 + 100 * row, 97 + 100 * col, 97 + 100 * row,
                                      fill=self.BALLS[player])
    def subscribe_to_mouse_click(self, observable):
        """Allow other parts of the program to subscribe to mouse click events."""
        # Store a weak reference to the observable to avoid strong reference issues
        self._mouse_click_observers.append(weakref.WeakMethod(observable))

    # def center_window(self):
    #     r"""
    #     tries to center window along screen dims;
    #
    #     no return value (void);
    #     """
    #     # ensure dims are correct
    #     self.update_idletasks()
    #     left = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
    #     top = (self.winfo_screenheight() - self.winfo_reqheight()) // 2
    #     self.geometry("+{x}+{y}".format(x=left, y=top))

    def initialize(self, initial_game_state):
        r"""
        widget's main inits;
        """
        # main window inits

        # set score callback method

        # self.grid.set_score_callback(self.update_score)
        self.withdraw()

        self.unbind_all("<Button-1>")
        self.listen = True

        # self.center_window()
        self.deiconify()
        self.game_state = initial_game_state
        # self.grid.reset_grid()
        # self.grid.set_game_state(self.game_state)
        # self.set_score(self.game_state.score)
        self.bind_all("<Button-1>", self._left_click_listener)


    def quit_app(self, **kw):
        r"""
        quit app dialog;
        """
        if tkinter.messagebox.askokcancel("Question", "Quit game?", parent=self):
            self._quit_game_callback()
            self.quit()

    def update_state(self, cor, turn):
        # row,col = state.move(1, action)
        print(cor)
        self.draw_ball(cor[0], cor[1], turn)
        # self.draw_ball(opponent_action[0], opponent_action[1], 2)
        # row,col = state.move(2, opponent_action)
        # self.draw_ball(row, col, 2)
        # if action == Action.LEFT:
        #     self.grid.move_tiles_left()
        # elif action == Action.RIGHT:
        #     self.grid.move_tiles_right()
        # elif action == Action.UP:
        #     self.grid.move_tiles_up()
        # elif action == Action.DOWN:
        #     self.grid.move_tiles_down()
        # elif action is Action.STOP:
        #     pass
        # else:
        #     raise Exception("Got unknown action.")
        # self.grid.insert_tile(opponent_action.row, opponent_action.column, opponent_action.value)
        self.mainloop_iteration()

    def mainloop_iteration(self):
        self.update_idletasks()
        self.update()



