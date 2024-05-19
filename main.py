import generate_strengths as gs
import generate_results as gr
import create_league as cl
import draw_tables_evolution as dte

def main():
    gs.main() #Generate the expected goals scored and conceded for each team based on season data 
    gr.main() #Generate the league fixtures and results
    cl.main() #Create league tables at the end of each round
    dte.main() #Plot the evolution of league standings during a season
    
if __name__ == "__main__":
    main()
