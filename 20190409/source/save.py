import os
import csv
import datetime


def save_vars():
    best_file_name = "Kospi_200_portfolio_optimization-GA_BEST.csv"
    test_file_name = "Kospi_200_portfolio_optimization-TEST.csv"
    variables = ['GLOBAL SETTINGS OF THE GA OPERATION']
    with open('../source/settings_rates.py', 'r') as variable_file:
        reader = csv.reader(variable_file)
        for row in reader:
            line = str(row)
            variables.append(line)

    if os.path.exists('../result/' + best_file_name):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    writer = csv.writer(open('../result/' + best_file_name, append_write, newline=''))
    writer.writerows([variables])

    if os.path.exists('../result/' + test_file_name):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    writer = csv.writer(open('../result/' + test_file_name, append_write, newline=''))
    writer.writerows([variables])

def save_population(pop, gen_number, year, month, training_file_name ):
    if os.path.exists('../result/' + str(year) + "/" + str(month) + '/' + training_file_name):
        append_write = 'a'  # append if already exists
    else:
        if not os.path.exists('../result/' + str(year) + "/" + str(month) + '/'):
            os.makedirs('../result/' + str(year) + "/" + str(month) + '/')
        append_write = 'w'  # make a new file if not
    writer = csv.writer(open('../result/' + str(year) + "/" + str(month) + '/' + training_file_name, append_write, newline=''))

    best_chromosome = pop.get_chromosomes()[0]
    tickers = best_chromosome.get_tickers()
    num_of_stocks = len(tickers)
    ticker_rows = []
    ticker_title = "Tradable Stock # " + str(num_of_stocks)
    ticker_rows.append(ticker_title)
    for num in range(num_of_stocks):
        ticker_rows.append(tickers[num])
    writer.writerows([ticker_rows])

    header_rows = []
    header_title = "Generation #" + str(gen_number)
    header_fitness_title = " | Fittest chromosome fitness: "
    header_fitness = best_chromosome.get_fitness()
    header_rows.append(header_title)
    for num in range(num_of_stocks):
        header_rows.append(best_chromosome.get_genes()[num])
    header_rows.append(header_fitness_title)
    header_rows.append(header_fitness)
    writer.writerows([header_rows])

    # for count in range(650):
    #     logging.info("=", end="")
    #     logging.info("")
    # logging.info(header_title, " - ", header_fitness_title, header_fitness)

    index = 0
    for chromosome in pop.get_chromosomes():
        chromosome_row = []
        chromosome_title = "Chromosome #" + str(index)
        chromosome_fitness_title = "Fitness"
        chromosome_roi_title = "ROI"
        chromosome_num_title = "Number of Stocks Selected"
        chromosome_row.append(chromosome_title)
        for num in range(num_of_stocks):
            chromosome_row.append(chromosome.get_genes()[num])
        chromosome_row.append(chromosome_fitness_title)
        chromosome_row.append(chromosome.get_fitness())
        chromosome_row.append(chromosome_roi_title)
        chromosome_row.append(chromosome.get_rois())
        chromosome_row.append(chromosome_num_title)
        chromosome_row.append(chromosome.get_num_of_selected_stocks())
        index += 1
        writer.writerows([chromosome_row])


def save_test_generation(best_chromosome, ga_start_date, ga_end_date, test_start_date, test_end_date, test_genes, test_roi, test_risk, test_fitness, test_term_return):
    best_file_name = "Kospi_200_portfolio_optimization-GA_BEST.csv"
    test_file_name = "Kospi_200_portfolio_optimization-TEST.csv"

    best = ["BEST GA"]
    genes_title = "Genes"
    fitness_title = "FITNESS"
    risk_title = "RISK"
    roi_title = "ROI"
    profit_title = "RETURN"
    best.append([str(ga_start_date), "~", str(ga_end_date)])
    best.append(genes_title)
    best.append(best_chromosome.get_genes())
    best.append(roi_title)
    best.append(best_chromosome.get_rois())
    best.append(risk_title)
    best.append(best_chromosome.get_risks())
    best.append(fitness_title)
    best.append(best_chromosome.get_fitness())
    writer = csv.writer(open('../result/' + best_file_name, 'a', newline=''))
    writer.writerows([best])

    test = ["TEST VALUES"]
    test.append([str(test_start_date), ",", str(test_end_date)])
    test.append(genes_title)
    test.append(test_genes)
    test.append(roi_title)
    test.append(test_roi)
    test.append(risk_title)
    test.append(test_risk)
    test.append(fitness_title)
    test.append(test_fitness)
    test.append(profit_title)
    test.append(test_term_return)
    writer = csv.writer(open('../result/' + test_file_name, 'a', newline=''))
    writer.writerows([test])


def print_test_population(best_chromosome, ga_start_date, ga_end_date, test_start_date, test_end_date, test_genes, test_num_of_selected_stocks, test_roi, test_risk, test_fitness):
    for count in range(650):
        print("=", end="")
    print()

    print("GA OPTIMIZATION ON KOSPI200 FINANCIAL DATA ON", ga_start_date, "~", ga_end_date)
    print("TEST ON KOSPI200 FINANCIAL DATA ON", test_start_date, "~", test_end_date, "USING GA RESULTS")
    for count in range(650):
        print("-", end="")
    print()
    print("BEST PF RESULT AFTER GA", best_chromosome, best_chromosome.get_genes(), "Number of stocks selected in the portfolio: ", best_chromosome.get_num_of_selected_stocks())
    print("TESTED GENES", test_genes, "Number of stocks selected in the portfolio: ", test_num_of_selected_stocks)
    print("GA ROI: ", best_chromosome.get_rois(), " | RISK: ", best_chromosome.get_risks())
    print("TEST ROI: ", test_roi, " | RISK: ", test_risk)
    print("GA Fittest chromosome fitness:", best_chromosome.get_fitness())
    print("TEST Fittest chromosome fitness:", test_fitness)

    for count in range(650):
        print("=", end="")
    print()

