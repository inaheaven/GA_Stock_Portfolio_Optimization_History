import os
import csv


def save_population(pop, gen_number, training_file_name, year, month):
    if os.path.exists('../result/' + str(year) + "/" + str(month) + '/' + training_file_name):
        append_write = 'a'  # append if already exists
    else:
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


def print_best_population(best_chromosome, ga_start_date, ga_end_date):
    for count in range(650):
        print("=", end="")
    print()
    print("GA OPTIMIZATION ON KOSPI200 FINANCIAL DATA ON", ga_start_date, "~", ga_end_date)
    print("BEST PF RESULT AFTER GA", best_chromosome, best_chromosome.get_genes())
    print("Number of stocks selected in the portfolio: ", best_chromosome.get_num_of_selected_stocks())
    print("ROI: ", best_chromosome.get_rois(), " | RISK: ", best_chromosome.get_risks())
    print("Fittest chromosome fitness:", best_chromosome.get_fitness())
    print()


def print_test_population(test_start_date, test_end_date, test_genes, test_num_of_selected_stocks, test_roi, test_risk, test_fitness):
    for count in range(650):
        print("-", end="")
    print()
    print("TEST ON KOSPI200 FINANCIAL DATA ON", test_start_date, "~", test_end_date, "USING GA RESULTS")
    print("BEST PF RESULT AFTER GA", test_genes)
    print("Number of stocks selected in the portfolio: ", test_num_of_selected_stocks)
    print("ROI: ", test_roi, " | RISK: ", test_risk)
    print("Fittest chromosome fitness:", test_fitness)
    print()
    for count in range(650):
        print("=", end="")
    print()


def save_best_generation(best_chromosome, year, month, monthly_best_file_name):
    monthly_best = []
    monthly_best_genes_title = "Genes"
    monthly_best_fitness_title = "FITNESS"
    monthly_best_roi_title = "ROI"
    monthly_best.append([year, month])
    monthly_best.append([monthly_best_genes_title, best_chromosome.get_genes()])
    monthly_best.append([monthly_best_fitness_title, best_chromosome.get_fitness()])
    monthly_best.append([monthly_best_roi_title, best_chromosome.get_rois()])
    writer = csv.writer(open('../result/' + str(year) + "/" + str(month) + '/' + monthly_best_file_name, 'a', newline=''))
    writer.writerows([monthly_best])


def save_vars(year, month, monthly_best_file_name):
    variables = ['GLOBAL SETTINGS OF THE OPERATION']
    with open('../source/settings_rates.py', 'r') as variable_file:
        reader = csv.reader(variable_file)
        for row in reader:
            line = str(row)
            variables.append(line)

    if os.path.exists('../result/' + str(year) + "/" + str(month) + '/' + monthly_best_file_name):
        append_write = 'a'  # append if already exists
    else:
        if not os.path.exists('../result/' + str(year) + "/" + str(month) + '/'):
            os.makedirs('../result/' + str(year) + "/" + str(month) + '/')
        append_write = 'w'  # make a new file if not
    writer = csv.writer(open('../result/' + str(year) + "/" + str(month) + '/' + monthly_best_file_name, append_write, newline=''))
    writer.writerows([variables])


