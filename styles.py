from tkinter import ttk 

def style(hgt,wdt):
    style = ttk.Style()
    style.theme_create( "dark_theme" ,"vista" ,  settings = {

          "root_menu.TFrame":{
                                "configure" : {"background" : "#434447"}
                           },
                           
          "root_main.TFrame":{
                                "configure" : {"background" : "#333333" }                      
                           },
 

          "root_status.TFrame":{
                                "configure" : {"background" : "#0b6faa"}
                           },
          "root_task.TFrame":{
                                "configure" : {"background" : "#96979c"},

                           },
          "root_task_cnt.TLabel":{
                                   "configure" : {"background" : "#434447" , "foreground" : "#d9cc99" , "font" : ('Tahoma',-int(hgt*0.025), 'bold') , "padding" : (int( 0.004*wdt) ,0 )}
                              },
          "root_theme.TCheckbutton":{
                                   "configure":{"background":"#434447" , "foreground" : "#B8B3BE"},
                                   },
          "root_theme.TLabel":{
                                   "configure":{"background":"#434447" , "foreground" : "#B8B3BE"},
                                   },
          "root_menu.TMenubutton":
                            {    
                                "configure" : {"font":('Tahoma', -int(hgt*0.024)) , "foreground":"#B8B3BE" , "background":"#434447" , "anchor":"center"},
                                "layout":[("Menubutton.background", None),("Menubutton.button", {"children":
                                                                                                            [("Menubutton.focus", {"children":
                                                                                                                                                [("Menubutton.padding" , {"children":
                                                                                                                                                                            [("Menubutton.label", {"side": "left", "expand": 1}
                                                                                                                                                                            )]
                                                                                                                                                                        }
                                                                                                                                                )]
                                                                                                                                    }
                                                                                                            )]
                                                                                                }
                                        )],
                                "map"       : {
                                            "background" : [("hover","#B8B3BE")],
                                            "foreground" : [("hover","#000")]

                                             }
                           },
          "status_text.TLabel":
                              {
                                   "configure" : {"background" : "#0b6faa" , "foreground" : "#f0f0f0" , "font" : ('Lucida Console',-int(hgt*0.02)) },
                              },

          "window_base.TFrame":{
                                "configure" : {"background" : "#fff"},

                           },
          "window_close.TLabel":
                                {
                                   "configure" : {"background" : "#434447" , "foreground" : "#d9cc99" , "font" : ('Tahoma',-int(hgt*0.024), 'bold') , "padding" : ( int(wdt*0.008), 0)},
                                   "map"       : {"background" : [('hover','red')]}

                                },
          
               
         "window_text.TLabel":
                                {
                                   "configure" : {"background" : "#333333" , "foreground" : "#d9cc99" , "font" : ('Lucida Console',-int(hgt*0.03)) },
                               },
          "window_btn.TButton":
                                {
                                   "configure" : {"background" : "#666666" , "foreground" : "#000" , "font" : ('Lucida Console',-int(hgt*0.03)) , "padding" : (int(wdt*0.002) , int(hgt*0.004)) },
                                   "map"       : {
                                            "background" : [("hover","#B8B3BE")],
                                            "foreground" : [("hover","red")]

                                             }
                               },
          
               
                         
        
    })


    style.theme_create( "light_theme" ,"vista" ,  settings = {
          "root_menu.TFrame":{
                                "configure" : {"background" : "#7ee8fa"}
                           },
          "root_main.TFrame":{
                                "configure" : {"background" : "#D0F4B9"}
                           },
          "root_status.TFrame":{
                                "configure" : {"background" : "#0b6faa"}
                           },
          "status_text.TLabel":
                              {
                                   "configure" : {"background" : "#0b6faa" , "foreground" : "#f0f0f0" , "font" : ('Lucida Console',-int(hgt*0.02)) },
                              },
          "root_task.TFrame":{
                                "configure" : {"background" : "#65caf6"},

                           },
          "root_task_cnt.TLabel":{
                                   "configure" : {"background" : "#7ee8fa" , "foreground" : "#000" , "font" : ('Tahoma',-int(hgt*0.025), 'bold') , "padding" : (int( 0.004*wdt) ,0 )}
                              },
          "root_theme.TCheckbutton":{
                                   "configure":{"background":"#7ee8fa" , "foreground" : "#B8B3BE"},
                                   },
          "root_theme.TLabel":{
                                   "configure":{"background":"#7ee8fa" , "foreground" : "#000"},
                                   },
          "root_menu.TMenubutton":
                            {    
                                "configure" : {"font":('Tahoma', -int(hgt*0.024)) , "foreground":"#3d3b30" , "background":"#7ee8fa" , "anchor":"center"},
                                "layout":[("Menubutton.background", None),("Menubutton.button", {"children":
                                                                                                            [("Menubutton.focus", {"children":
                                                                                                                                                [("Menubutton.padding" , {"children":
                                                                                                                                                                            [("Menubutton.label", {"side": "left", "expand": 1}
                                                                                                                                                                            )]
                                                                                                                                                                        }
                                                                                                                                                )]
                                                                                                                                    }
                                                                                                            )]
                                                                                                }
                                        )],
                                "map"       : {
                                            "background" : [("hover","#ADFC92")],
                                            "foreground" : [("hover","#000")]

                                             }
                           },
          "window_base.TFrame":{
                                "configure" : {"background" : "#000"},

                           },
          "window_close.TLabel":
                                {
                                    "configure" : {"background" : "#7ee8fa" , "foreground" : "#fff" , "font" : ('Tahoma',-int(hgt*0.024), 'bold'), "padding" : ( int(wdt*0.008), 0) },
                                    "map"       : {"background" : [('hover','red')]}

                                },
               
         "window_text.TLabel":
                                {
                                   "configure" : {"background" : "#D0F4B9" , "foreground" : "#000" , "font" : ('Lucida Console',-int(hgt*0.03)) },
                               },
          "window_btn.TButton":
                                {
                                   "configure" : {"background" : "#CAEDF6" , "foreground" : "#000" , "font" : ('Lucida Console',-int(hgt*0.03)) , "padding" : (int(wdt*0.003) , int(hgt*0.008)) , "relief" : "solid" },
                                   "map"       : {
                                            "background" : [("hover","#ADFC92")],
                                            "foreground" : [("hover","red")]

                                             }
                               },
          
 
    })
    return(style)
