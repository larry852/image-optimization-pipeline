import csv


def main():
    init_file_analysis()
    counter_improvement = 0
    counter_improvement_equal = 0
    improvement_pipelines = []
    improvement_equal_pipelines = []
    with open('results.csv', 'r') as csv_file:
        results = list(csv.reader(csv_file))
        del results[0]

        for result in results:
            if result[1] == 'original':
                image = result[0]
                pipelines = [row for row in results if row[0] == image and row[1] != 'original']

                max_percentage = max([int(percentage[2]) for percentage in pipelines])
                difference = max_percentage - int(result[2])
                write_file_analysis([image, result[2], max_percentage, difference])
                for pipeline in pipelines:
                    if int(pipeline[2]) > int(result[2]):
                        counter_improvement += 1
                        improvement_pipelines.append(pipeline[1])
                    if int(pipeline[2]) >= int(result[2]):
                        counter_improvement_equal += 1
                        improvement_equal_pipelines.append(pipeline[1])

        print('Total pipelines generados: {}'.format(len(results)))
        print('Total pipelines que aumentaron el porcentaje original: {}'.format(counter_improvement))
        print('Pipeline que aumento porcentaje original mas frecuente: [{}]'.format(max(improvement_pipelines, key=improvement_pipelines.count).replace('\n', ', ')))
        print('Total pipelines aumentaron o igualaron el porcentaje original: {}'.format(counter_improvement_equal))
        print('Pipeline que aumento o igualó porcentaje original mas frecuente: [{}]'.format(max(improvement_pipelines, key=improvement_pipelines.count).replace('\n', ', ')))
    csv_file.close()


def init_file_analysis():
    with open('analysis.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['IMAGEN', 'ORIGINAL', 'PIPELINE', 'DIFERENCIA'])
    csv_file.close()


def write_file_analysis(row):
    with open('analysis.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    csv_file.close()


if __name__ == '__main__':
    main()
