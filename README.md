Flashlight
==========

Flashlight is an **unofficial Spotlight API** that allows you to programmatically process queries and add additional results. It's *very rough right now,* and a *horrendous hack*, but a fun proof of concept.

**Installation**

Flashlight depends on [EasySIMBL](https://github.com/norio-nomura/EasySIMBL), a runtime code-injection framework. (like MobileSubstrate, but for OS X). 

When you build and run the Xcode project, it generates a bundle called `SpotlightSIMBL.bundle`, automatically copies it to `~/Library/Application Support/SIMBL/Plugins`, then restarts Spotlight.

**API**

After installation, Flashlight reads plugins from `~/Library/FlashlightPlugins`. Each plugin must be a directory containing an executable named `executable`.

Every time you type a character into Spotlight, each plugin's executable will be invoked with your query as the first argument (`argv[1]`). If the plugin decides to respond to the query, it should print a json document to `stdout` in this format:

```
{
	"title": "'Hello world' in Pig Latin",
	"html": "<h1>ellohay, orldway</h1>",
	"execute": "(shell string to execute when enter is pressed)"
}
```

(if the plugin doesn't want to provide a response, just don't print anything.)

This HTML will then be presented to the user:

![Image of a Spotlight window showing 'ellohay orldway' as the Pig Latin translation of 'hello world'](https://raw.github.com/nate-parrott/flashlight/master/PigLatinExampleImage.png)

(this HTML will be loaded with the plugin's directory as its base URL, so you can reference images, javascript and CSS from it.)

This is currently all the API does. More capabilities, like more customization of the search result, are on my to-do list.

**How it works**

The `Flashlight.app` Xcode target is a fork of [EasySIMBL](https://github.com/norio-nomura/EasySIMBL) (which is designed to allow loading runtime injection of plugins into arbitrary apps) that's been modified to load a single plugin (stored inside its own bundle, rather than an external directory) into the Spotlight process. It should be able to coexist with EasySIMBL if you use it.

The SIMBL plugin that's loaded into Spotlight, `SpotlightSIMBL.bundle`, patches Spotlight to add a new subclass of `SPQuery`, the internal class used to fetch results from different sources. It runs executables in `~/Library/FlashlightPlugins/*/executable`, and then presents their results using a custom subclass of `SPResult`.

Since [I'm not sure how to subclass classes that aren't available at link time](http://stackoverflow.com/questions/26704130/subclass-objective-c-class-without-linking-with-the-superclass), subclasses of Spotlight internal classes are made at runtime using [Mike Ash's instructions and helper code](https://www.mikeash.com/pyblog/friday-qa-2010-11-19-creating-classes-at-runtime-for-fun-and-profit.html).

The Spotlight plugin is gated to run only on version `911` (which ships in Yosemite 14A361c). If a new version of Spotlight comes out, you can manually edit `SpotlightSIMBL/SpotlightSIMBL/Info.plist` key `SIMBLTargetApplications.MaxBundleVersion`, restarts Spotlight, verify everything works, and then submit a pull request.
