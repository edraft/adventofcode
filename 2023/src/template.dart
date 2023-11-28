import 'aoc/helper.dart';

String input = "";

void firstPart() {}

void secondPart() {}

Future<void> main(List<String> args) async {
  if (args.isEmpty) {
    print("Expected day");
    return;
  }

  int year = int.parse(args[0]);
  int day = int.parse(args[1]);

  input = await getInput(year, day);
  print('Advent of code $year day $day');
  firstPart();
  secondPart();
}
