import os
target_name = os.path.join(os.path.dirname(__file__), 'STAR_OEM.hsl')
prefix = r"""namespace _Method { #include "HSLHttp\\HSLHttp.hsl" } 
namespace _Method { #include "HSLJson\\HSLJson.hsl" } 
namespace _Method { #include "STAR_OEM_toolkit.hs_" } 
namespace _Method { #include "HSLStrLib.hsl" } 
namespace _Method { #include "HSLTrcLib.hsl" } 
namespace _Method { #include "HSLSeqLib.hsl" } 
namespace _Method { #include "HSLDevLib.hsl" } 
namespace _Method { #include "ASWStandard\\TraceLevel\\TraceLevel.hsl" } 
namespace _Method { #include "HslHamHeaterShakerLib.hsl" } 
namespace _Method { #include "HSLJson\\HSLJson.hsl" } 
#include "STAR_OEM.res"
variable loopCounterMain;
variable msg;
object objJSONFromServer;
variable commandFromServer;
variable initializeAlways;
variable o_stepReturn1_t1;
variable o_stepReturn2_t1;
variable o_stepReturn3_t1;
object objJSONToServer;
sequence seq;
variable tipSequence;
variable sequenceCounting;
variable channelVariable;
variable channelUse;
variable labwarePositions;
variable aspirateSequence;
variable v;
variable arrayOfVolumes[];
variable liquidClass;
variable aspirateMode;
variable capacitiveLLD;
variable pressureLLD;
variable liquidFollowing;
variable submergeDepth;
variable liquidHeight;
variable maxLLdDifference;
variable mixCycles;
variable mixPosition;
variable mixVolume;
variable airTransportRetractDist;
variable touchOff;
variable aspPosAboveTouch;
variable o_liquidLevels_mm[];
variable o_liquidLevels_mL[];
variable dispenseMode;
variable dispenseSequence;
variable dispPositionAboveTouch;
variable zMoveAfterStep;
variable sideTouch;
variable wasteSequence;
variable useDefaultWaste;
variable reducedPatternMode;
variable aspirateVolume;
variable o_stepReturn1_t14;
variable dispenseVolume;
variable tipEjectToKnownPosition;
variable carrierName;
variable barcodeFileName;
variable barcodeReadPositions;
variable o_carrierBC;
variable o_carrierPositionsBCs[];
variable lidSequence;
variable plateSequence;
variable toolSequence;
variable transportMode;
variable widthBefore;
variable gripHeight;
variable gripWidth;
variable gripSpeed;
variable gripperToolChannel;
variable checkPlate;
variable zSpeed;
variable gripForce;
sequence lidSeq;
sequence toolSeq;
variable xAcceleration;
variable platePressOnDistance;
variable ejectToolWhenFinish;
object objHttp;
variable blnReturn;
variable blnSuccess;
variable usedNode;
variable deviceNumber;
variable action;
variable sampleInterval;
variable shakingToleranceRange;
variable id;
global device ML_STAR ("STAR_OEM.lay", "ML_STAR", hslTrue);
variable monitorResult;
variable firmwareVersion;
variable serialNumber;
variable command;
variable parameter;
variable plateLock;
variable shakingAccRamp;
variable shakingDirection;
variable simulate;
variable startTimeout;
variable toleranceRange;
variable securityRange;
variable intTrace;
variable shakingSpeed;
variable shakingTime;
variable temperature;
variable waitForTempReached;
variable inverseGrip;
variable liftUpHeight;
variable retractDistance;
variable tolerance;
variable labwareOrientation;
variable movementType;
variable collisionControl;
variable gripMode;
variable showCollisionCheckDialog;
global device HxFan ("STAR_OEM.lay", "HxFan", hslTrue);
variable fanSpeed;
variable persistant;
variable refillAfterEmpty;
variable chamber1LiquidChange;
variable chamber2WashLiquid;
variable chamber1WashLiquid;
variable chamber2LiquidChange;
variable rc(0);
variable timeout(2*60);
variable handle;
variable handles[ ];
variable argument_t1;
variable arguments_t1[];
namespace _Method { #include "HSLMETEDLib.hs_" } 
namespace _Method { #include "HSLMECCLib.hs_" } 
namespace _Method { #include "HSLSTCCLib.hs_" } 

namespace _Method {  #include __filename__ ".sub"  }

namespace _Method { method main(  ) void {
        STAR_OEM_TOOLKIT::_InitLibrary();
        ::RegisterAbortHandler( "OnAbort");
        blnReturn = HSLHttp::Initialize(objHttp);
        if (blnReturn != blnSuccess)
        {
            TRACELEVEL::Trace_04(TRACE_LEVEL_RELEASE, Translate("HTTP Test Method"), Translate(" - "), Translate("Error Initializing HTTP Library"), Translate(""));
            return;
        }
        SendTextMessageToServer(Translate("Hi, I´m a VENUS method."));
        onerror goto ErrorHandler;
        {
            loopCounterMain = 0;
            while (1 == 1)
            {
                loopCounterMain = loopCounterMain + 1;

                commandFromServer = Translate("");
                o_stepReturn1_t1 = Translate("");
                o_stepReturn2_t1 = Translate("");
                o_stepReturn3_t1 = Translate("");
                o_stepReturn1_t14 = Translate("");


                msg = waitForGUItoContinue();
                Trace("JSON received from Server:", msg);
                HSLJsonLib::Create(objJSONFromServer);
                HSLJsonLib::ParseJson(objJSONFromServer, msg);
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("command"), commandFromServer);
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("id"), id);

                
                handle = Fork("doCommand");
                if (0 == handle)
                err.Raise(0, "Failed to fork doCommand");
                handles.AddAsLast(handle);
                
                // do anything else in the main thread

                rc = Join(handles, timeout);
                if (0 == rc)
                err.Raise(1, "Failed to join handles");
                HSLJsonLib::Release(objJSONFromServer);

                if (commandFromServer == "end")
                {
                    SendTextMessageToServer(Translate("Good Bye!"));
                    break;
                }

            }
        }
        HSLHttp::Release(objHttp);
        STAR_OEM_TOOLKIT::_ExitLibrary();
        return;
        ErrorHandler :
        {
            if (hslAbort == MessageBox( err.GetDescription(), "Error - Main", hslError|hslAbortRetryIgnore))
            abort;
            resume next;
        }
    }
}

namespace _Method { function doCommand()
    {
        
        


        if (commandFromServer == "initialize")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("initializeAlways"), argument_t1);
            arguments_t1.AddAsLast(argument_t1);
            STAR_OEM_TOOLKIT::Initialize(ML_STAR, arguments_t1.GetAt(0), o_stepReturn1_t1);
            TrcTrace(Translate("Init step return:"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }



        if (commandFromServer == "channelTipPickUp")
        {
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("tipSequence"), tipSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("channelVariable"), channelVariable);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("channelUse"), channelUse);
            if (tipSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("labwarePositions"), labwarePositions);
                BuildTempSequenceFromPositions(labwarePositions, seq);
            }
            else
            {
                DevGetSequenceRef(ML_STAR, tipSequence, seq);
            }
            STAR_OEM_TOOLKIT::Channels_1mL_TipPickUp(ML_STAR, seq, channelVariable, sequenceCounting, channelUse, o_stepReturn1_t1);
            TrcTrace(Translate("Tip pick up step return:"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "channelAspirate")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("aspirateSequence"), aspirateSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("channelVariable"), channelVariable);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("channelUse"), channelUse);
            BuildArrayOfVolumesForChannels(channelVariable, arrayOfVolumes);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("liquidClass"), liquidClass);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("aspirateMode"), aspirateMode);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("capacitiveLLD"), capacitiveLLD);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("pressureLLD"), pressureLLD);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("liquidFollowing"), liquidFollowing);
            Trace("Bookstart");
            JSON_GetFloatValue(Translate("submergeDepth"), submergeDepth);
            Trace("Bookend");
            JSON_GetFloatValue(Translate("liquidHeight"), liquidHeight);
            JSON_GetFloatValue(Translate("maxLLdDifference"), maxLLdDifference);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("mixCycles"), mixCycles);
            JSON_GetFloatValue(Translate("mixPosition"), mixPosition);
            JSON_GetFloatValue(Translate("mixVolume"), mixVolume);
            JSON_GetFloatValue(Translate("airTransportRetractDist"), airTransportRetractDist);
            JSON_GetFloatValue(Translate("aspPosAboveTouch"), aspPosAboveTouch);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("touchOff"), touchOff);

            if (aspirateSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("labwarePositions"), labwarePositions);
                BuildTempSequenceFromPositions(labwarePositions, seq);
            }
            else
            {
                DevGetSequenceRef(ML_STAR, aspirateSequence, seq);
            }
            STAR_OEM_TOOLKIT::Channels_1ml_Aspirate(ML_STAR, seq, arrayOfVolumes, channelVariable, liquidClass, sequenceCounting, channelUse, aspirateMode, capacitiveLLD, pressureLLD, liquidFollowing, submergeDepth, liquidHeight, maxLLdDifference, mixCycles, mixPosition, mixVolume, airTransportRetractDist, touchOff, aspPosAboveTouch, o_stepReturn1_t1, o_liquidLevels_mm, o_liquidLevels_mL);
            ArrayToString(o_liquidLevels_mm, o_stepReturn2_t1);
            ArrayToString(o_liquidLevels_mL, o_stepReturn3_t1);
            TrcTrace(Translate("Aspirate step return 1:"), o_stepReturn1_t1);
            TrcTrace(Translate("Aspirate step return 2:"), o_stepReturn2_t1);
            TrcTrace(Translate("Aspirate step return 3:"), o_stepReturn3_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, Translate(""), id);
        }


        if (commandFromServer == "channelDispense")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("dispenseSequence"), dispenseSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("channelVariable"), channelVariable);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("channelUse"), channelUse);
            BuildArrayOfVolumesForChannels(channelVariable, arrayOfVolumes);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("liquidClass"), liquidClass);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("dispenseMode"), dispenseMode);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("capacitiveLLD"), capacitiveLLD);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("liquidFollowing"), liquidFollowing);
            JSON_GetFloatValue(Translate("submergeDepth"), submergeDepth);
            JSON_GetFloatValue(Translate("liquidHeight"), liquidHeight);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("mixCycles"), mixCycles);
            JSON_GetFloatValue(Translate("mixPosition"), mixPosition);
            JSON_GetFloatValue(Translate("mixVolume"), mixVolume);
            JSON_GetFloatValue(Translate("airTransportRetractDist"), airTransportRetractDist);
            JSON_GetFloatValue(Translate("dispPositionAboveTouch"), dispPositionAboveTouch);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("touchOff"), touchOff);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("zMoveAfterStep"), zMoveAfterStep);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sideTouch"), sideTouch);

            if (dispenseSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("labwarePositions"), labwarePositions);
                BuildTempSequenceFromPositions(labwarePositions, seq);
            }
            else
            {
                DevGetSequenceRef(ML_STAR, dispenseSequence, seq);
            }
            STAR_OEM_TOOLKIT::Channels_1mL_Dispense(ML_STAR, seq, arrayOfVolumes, channelVariable, liquidClass, sequenceCounting, channelUse, dispenseMode, capacitiveLLD, liquidFollowing, submergeDepth, liquidHeight, mixCycles, mixPosition, mixVolume, airTransportRetractDist, touchOff, zMoveAfterStep, sideTouch, dispPositionAboveTouch, o_stepReturn1_t1, o_liquidLevels_mm, o_liquidLevels_mL);
            ArrayToString(o_liquidLevels_mm, o_stepReturn2_t1);
            ArrayToString(o_liquidLevels_mL, o_stepReturn3_t1);
            TrcTrace(Translate("Aspirate step return 1:"), o_stepReturn1_t1);
            TrcTrace(Translate("Aspirate step return 2:"), o_stepReturn2_t1);
            TrcTrace(Translate("Aspirate step return 3:"), o_stepReturn3_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, Translate(""), id);
        }


        if (commandFromServer == "channelTipEject")
        {
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("wasteSequence"), wasteSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("channelVariable"), channelVariable);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("channelUse"), channelUse);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("useDefaultWaste"), useDefaultWaste);
            if (useDefaultWaste == 0)
            {
                if (wasteSequence == "")
                {
                    HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("labwarePositions"), labwarePositions);
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
                else
                {
                    DevGetSequenceRef(ML_STAR, wasteSequence, seq);
                }
            }
            else
            {
                SeqCopySequence(seq, ML_STAR.Waste);
            }
            STAR_OEM_TOOLKIT::Channels_1mL_TipEject(ML_STAR, seq, channelVariable, sequenceCounting, channelUse, useDefaultWaste, o_stepReturn1_t1);
            TrcTrace(Translate("Tip eject step return:"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }




        if (commandFromServer == "mph96TipPickUp")
        {
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("tipSequence"), tipSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("channelVariable"), channelVariable);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("reducedPatternMode"), reducedPatternMode);
            if (tipSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("labwarePositions"), labwarePositions);
                BuildTempSequenceFromPositions(labwarePositions, seq);
            }
            else
            {
                DevGetSequenceRef(ML_STAR, tipSequence, seq);
            }
            STAR_OEM_TOOLKIT::MPH96_TipPickUp(ML_STAR, seq, channelVariable, sequenceCounting, reducedPatternMode, o_stepReturn1_t1, o_stepReturn2_t1);
            TrcTrace(Translate("Tip pick up step return:"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, Translate(""), Translate(""), id);
        }


        if (commandFromServer == "mph96Aspirate")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("aspirateSequence"), aspirateSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("channelVariable"), channelVariable);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            JSON_GetFloatValue(Translate("aspirateVolume"), aspirateVolume);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("liquidClass"), liquidClass);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("aspirateMode"), aspirateMode);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("capacitiveLLD"), capacitiveLLD);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("liquidFollowing"), liquidFollowing);
            JSON_GetFloatValue(Translate("submergeDepth"), submergeDepth);
            JSON_GetFloatValue(Translate("liquidHeight"), liquidHeight);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("mixCycles"), mixCycles);
            JSON_GetFloatValue(Translate("mixPosition"), mixPosition);
            JSON_GetFloatValue(Translate("mixVolume"), mixVolume);
            JSON_GetFloatValue(Translate("airTransportRetractDist"), airTransportRetractDist);

            if (aspirateSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("labwarePositions"), labwarePositions);
                BuildTempSequenceFromPositions(labwarePositions, seq);
            }
            else
            {
                DevGetSequenceRef(ML_STAR, aspirateSequence, seq);
            }
            STAR_OEM_TOOLKIT::MPH96_Aspirate(ML_STAR, seq, aspirateVolume, channelVariable, liquidClass, sequenceCounting, aspirateMode, capacitiveLLD, liquidFollowing, submergeDepth, liquidHeight, mixCycles, mixPosition, mixVolume, airTransportRetractDist, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, o_stepReturn1_t14);
            TrcTrace(Translate("Aspirate step return 1:"), o_stepReturn1_t1);
            TrcTrace(Translate("Aspirate step return 2:"), o_stepReturn2_t1);
            TrcTrace(Translate("Aspirate step return 3:"), o_stepReturn3_t1);
            TrcTrace(Translate("Aspirate step return 3:"), o_stepReturn1_t14);
            o_stepReturn2_t1 = StrFStr(o_stepReturn2_t1);
            o_stepReturn3_t1 = StrFStr(o_stepReturn3_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, o_stepReturn1_t14, id);
        }


        if (commandFromServer == "mph96Dispense")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("dispenseSequence"), dispenseSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("channelVariable"), channelVariable);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            JSON_GetFloatValue(Translate("dispenseVolume"), dispenseVolume);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("liquidClass"), liquidClass);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("dispenseMode"), dispenseMode);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("capacitiveLLD"), capacitiveLLD);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("liquidFollowing"), liquidFollowing);
            JSON_GetFloatValue(Translate("submergeDepth"), submergeDepth);
            JSON_GetFloatValue(Translate("liquidHeight"), liquidHeight);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("mixCycles"), mixCycles);
            JSON_GetFloatValue(Translate("mixPosition"), mixPosition);
            JSON_GetFloatValue(Translate("mixVolume"), mixVolume);
            JSON_GetFloatValue(Translate("airTransportRetractDist"), airTransportRetractDist);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("zMoveAfterStep"), zMoveAfterStep);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sideTouch"), sideTouch);

            if (dispenseSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("labwarePositions"), labwarePositions);
                BuildTempSequenceFromPositions(labwarePositions, seq);
            }
            else
            {
                DevGetSequenceRef(ML_STAR, dispenseSequence, seq);
            }
            STAR_OEM_TOOLKIT::MPH96_Dispense(ML_STAR, seq, dispenseVolume, liquidClass, sequenceCounting, dispenseMode, capacitiveLLD, liquidFollowing, submergeDepth, liquidHeight, mixCycles, mixPosition, mixVolume, airTransportRetractDist, zMoveAfterStep, sideTouch, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, o_stepReturn1_t14);
            TrcTrace(Translate("Aspirate step return 1:"), o_stepReturn1_t1);
            TrcTrace(Translate("Aspirate step return 2:"), o_stepReturn2_t1);
            TrcTrace(Translate("Aspirate step return 3:"), o_stepReturn3_t1);
            TrcTrace(Translate("Aspirate step return 4:"), o_stepReturn1_t14);
            o_stepReturn2_t1 = StrFStr(o_stepReturn2_t1);
            o_stepReturn3_t1 = StrFStr(o_stepReturn3_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, o_stepReturn1_t14, id);
        }


        if (commandFromServer == "mph96TipEject")
        {
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("wasteSequence"), wasteSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("channelVariable"), channelVariable);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("tipEjectToKnownPosition"), tipEjectToKnownPosition);
            if (tipEjectToKnownPosition == 0)
            {
                if (wasteSequence == "")
                {
                    HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("labwarePositions"), labwarePositions);
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
                else
                {
                    DevGetSequenceRef(ML_STAR, wasteSequence, seq);
                }
            }
            else
            {
                SeqCopySequence(seq, ML_STAR.Waste);
            }
            STAR_OEM_TOOLKIT::MPH96_TipEject(ML_STAR, seq, sequenceCounting, tipEjectToKnownPosition, o_stepReturn1_t1, o_stepReturn2_t1);
            TrcTrace(Translate("Tip eject MPH96 step return:"), o_stepReturn1_t1);
            TrcTrace(Translate("Tip eject MPH96 step return2:"), o_stepReturn2_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, Translate(""), Translate(""), id);
        }



        if (commandFromServer == "loadCarrier")
        {
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("carrierName"), carrierName);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("barcodeFileName"), barcodeFileName);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("barcodeReadPositions"), barcodeReadPositions);
            STAR_OEM_TOOLKIT::Carrier_Load(ML_STAR, carrierName, barcodeFileName, barcodeReadPositions, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, o_stepReturn1_t14, o_carrierBC, o_carrierPositionsBCs);
            TrcTrace(Translate("Load carrier step return:"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, o_stepReturn1_t14, id);
        }


        if (commandFromServer == "unloadCarrier")
        {
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("carrierName"), carrierName);
            STAR_OEM_TOOLKIT::Carrier_Unload(ML_STAR, carrierName, o_stepReturn1_t1);
            TrcTrace(Translate("Unload Carrier step return:"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }



        if (commandFromServer == "gripGet")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateSequence"), plateSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("lidSequence"), lidSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("toolSequence"), toolSequence);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("transportMode"), transportMode);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("gripForce"), gripForce);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("gripperToolChannel"), gripperToolChannel);
            JSON_GetFloatValue(Translate("gripWidth"), gripWidth);
            JSON_GetFloatValue(Translate("gripHeight"), gripHeight);
            JSON_GetFloatValue(Translate("widthBefore"), widthBefore);
            JSON_GetFloatValue(Translate("gripSpeed"), gripSpeed);
            JSON_GetFloatValue(Translate("zSpeed"), zSpeed);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("checkPlate"), checkPlate);

            if (plateSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, plateSequence, seq);
            }
            if (lidSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("lidLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, lidSequence, lidSeq);
            }
            DevGetSequenceRef(ML_STAR, toolSequence, toolSeq);
            STAR_OEM_TOOLKIT::Channels_1mL_COREGrippers_Get(ML_STAR, seq, lidSeq, toolSeq, sequenceCounting, transportMode, gripForce, gripperToolChannel, gripWidth, gripHeight, widthBefore, gripSpeed, zSpeed, checkPlate, o_stepReturn1_t1);
            TrcTrace(Translate("Channel 1mL -  CO-RE Gripper Get - step return :"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "gripMove")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateSequence"), plateSequence);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("xAcceleration"), xAcceleration);

            if (plateSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, plateSequence, seq);
            }
            STAR_OEM_TOOLKIT::Channels_1mL_COREGrippers_Move(ML_STAR, seq, xAcceleration, o_stepReturn1_t1);
            TrcTrace(Translate("Channel 1mL -  CO-RE Gripper Move - step return:"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "gripPlace")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateSequence"), plateSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("lidSequence"), lidSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("toolSequence"), toolSequence);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("transportMode"), transportMode);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("ejectToolWhenFinish"), ejectToolWhenFinish);
            JSON_GetFloatValue(Translate("zSpeed"), zSpeed);
            JSON_GetFloatValue(Translate("platePressOnDistance"), platePressOnDistance);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("xAcceleration"), xAcceleration);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("checkPlate"), checkPlate);

            if (plateSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, plateSequence, seq);
            }
            if (lidSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("lidLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, lidSequence, lidSeq);
            }
            DevGetSequenceRef(ML_STAR, toolSequence, toolSeq);
            STAR_OEM_TOOLKIT::Channels_1mL_COREGrippers_Place(ML_STAR, seq, lidSeq, toolSeq, sequenceCounting, transportMode, ejectToolWhenFinish, zSpeed, platePressOnDistance, xAcceleration, checkPlate, o_stepReturn1_t1);
            TrcTrace(Translate("Channel 1mL -  CO-RE Gripper Place - step return :"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }




        if (commandFromServer == "iSwapGet")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateSequence"), plateSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("lidSequence"), lidSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("toolSequence"), toolSequence);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("movementType"), movementType);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("transportMode"), transportMode);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("labwareOrientation"), labwareOrientation);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("gripForce"), gripForce);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("inverseGrip"), inverseGrip);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("collisionControl"), collisionControl);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("gripMode"), gripMode);
            JSON_GetFloatValue(Translate("retractDistance"), retractDistance);
            JSON_GetFloatValue(Translate("liftUpHeight"), liftUpHeight);
            JSON_GetFloatValue(Translate("gripWidth"), gripWidth);
            JSON_GetFloatValue(Translate("tolerance"), tolerance);
            JSON_GetFloatValue(Translate("gripHeight"), gripHeight);
            JSON_GetFloatValue(Translate("widthBefore"), widthBefore);

            if (plateSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, plateSequence, seq);
            }
            if (lidSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("lidLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, lidSequence, lidSeq);
            }
            STAR_OEM_TOOLKIT::iSWAP_Get(ML_STAR, seq, lidSeq, sequenceCounting, movementType, transportMode, labwareOrientation, gripForce, inverseGrip, collisionControl, gripMode, retractDistance, liftUpHeight, gripWidth, tolerance, gripHeight, widthBefore, o_stepReturn1_t1);
            TrcTrace(Translate("iSWAP Get - step return :"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "iSwapMove")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateSequence"), plateSequence);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("collisionControl"), collisionControl);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("gripMode"), gripMode);

            if (plateSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, plateSequence, seq);
            }
            STAR_OEM_TOOLKIT::iSWAP_Move(ML_STAR, seq, collisionControl, gripMode, o_stepReturn1_t1);
            TrcTrace(Translate("iSWAP Move - step return :"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "iSwapPlace")
        {

            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateSequence"), plateSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("lidSequence"), lidSequence);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("toolSequence"), toolSequence);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sequenceCounting"), sequenceCounting);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("movementType"), movementType);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("transportMode"), transportMode);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("labwareOrientation"), labwareOrientation);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("collisionControl"), collisionControl);
            JSON_GetFloatValue(Translate("retractDistance"), retractDistance);
            JSON_GetFloatValue(Translate("liftUpHeight"), liftUpHeight);

            if (plateSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("plateLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, plateSequence, seq);
            }
            if (lidSequence == "")
            {
                HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("lidLabwarePositions"), labwarePositions);
                if (labwarePositions != "")
                {
                    BuildTempSequenceFromPositions(labwarePositions, seq);
                }
            }
            else
            {
                DevGetSequenceRef(ML_STAR, lidSequence, lidSeq);
            }
            STAR_OEM_TOOLKIT::iSWAP_Place(ML_STAR, seq, lidSeq, sequenceCounting, movementType, transportMode, labwareOrientation, collisionControl, retractDistance, liftUpHeight, o_stepReturn1_t1);
            TrcTrace(Translate("iSWAP Place - step return :"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "iSwapPark")
        {

            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("showCollisionCheckDialog"), showCollisionCheckDialog);

            STAR_OEM_TOOLKIT::iSWAP_Park(ML_STAR, showCollisionCheckDialog, o_stepReturn1_t1);
            TrcTrace(Translate("iSWAP Park - step return :"), o_stepReturn1_t1);
            SendStepReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }




        if (commandFromServer == "HHS_BeginMonitoring")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("shakingToleranceRange"), shakingToleranceRange);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("sampleInterval"), sampleInterval);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("action"), action);
            o_stepReturn1_t1 = 0;
            onerror goto errLabel_3202FD4CC34D478f892F31C7684340BE ;
            err.Clear();
            HSLHamHeaterShaker::BeginMonitoring(deviceNumber, shakingToleranceRange, sampleInterval, action);
            errLabel_3202FD4CC34D478f892F31C7684340BE : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            TrcTrace(Translate("HHS create STAR device step return:"), o_stepReturn1_t1);
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_CreateStarDevice")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("usedNode"), usedNode);
            onerror goto errLabel_18D9C44C12554d56B5C39C21EA142EC8 ;
            err.Clear();
            o_stepReturn1_t1 = HSLHamHeaterShaker::CreateStarDevice(ML_STAR, usedNode, deviceNumber);
            errLabel_18D9C44C12554d56B5C39C21EA142EC8 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            TrcTrace(Translate("HHS create STAR device step return:"), o_stepReturn1_t1);
            TrcTrace(Translate("HHS create STAR device step return2 (device number):"), deviceNumber);
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, deviceNumber, Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_CreateUSBDevice")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("usedNode"), usedNode);
            onerror goto errLabel_98100824AA704d26AB40A6BADEF39F48 ;
            err.Clear();
            o_stepReturn1_t1 = HSLHamHeaterShaker::CreateUsbDevice(usedNode, deviceNumber);
            errLabel_98100824AA704d26AB40A6BADEF39F48 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            TrcTrace(Translate("HHS create USB device step return:"), o_stepReturn1_t1);
            TrcTrace(Translate("HHS create USB device step return2 (device number):"), deviceNumber);
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, deviceNumber, Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_EndMonitoring")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_DE0DE7FF7B3F4304A0257A082FAC9714 ;
            err.Clear();
            o_stepReturn1_t1 = HSLHamHeaterShaker::EndMonitoring(deviceNumber, monitorResult);
            errLabel_DE0DE7FF7B3F4304A0257A082FAC9714 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            TrcTrace(Translate("HHS End Monitoring step return:"), o_stepReturn1_t1);
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, monitorResult, Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_GetFirmwareVersion")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_8E6D8176362E4b22B89EBFFEECC84662 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            HSLHamHeaterShaker::GetFirmwareVersion(deviceNumber, firmwareVersion);
            errLabel_8E6D8176362E4b22B89EBFFEECC84662 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, firmwareVersion, Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_GetSerialNumber")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_1EA05DE4F8124126A4D3AD21F777FDD5 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            HSLHamHeaterShaker::GetSerialNumber(deviceNumber, serialNumber);
            errLabel_1EA05DE4F8124126A4D3AD21F777FDD5 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, serialNumber, Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_GetShakerParameter")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_181E92C6D8E348c483BFCD0F16D88AB3 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            HSLHamHeaterShaker::GetShakerParameter(deviceNumber, o_stepReturn2_t1, o_stepReturn3_t1);
            errLabel_181E92C6D8E348c483BFCD0F16D88AB3 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, Translate(""), id);
        }


        if (commandFromServer == "HHS_GetShakerSpeed")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_C342F6DC97064debAC7DC78E54AD4F78 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::GetShakerSpeed(deviceNumber, o_stepReturn2_t1);
            errLabel_C342F6DC97064debAC7DC78E54AD4F78 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, Translate(""), id);
        }


        if (commandFromServer == "HHS_GetTempParameter")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_C16E1CF8298042f0A01D1040DC911015 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            HSLHamHeaterShaker::GetTempParameter(deviceNumber, o_stepReturn2_t1, o_stepReturn3_t1, o_stepReturn1_t14);
            errLabel_C16E1CF8298042f0A01D1040DC911015 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, o_stepReturn3_t1, Translate(""), id);
        }


        if (commandFromServer == "HHS_GetTemperature")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_14A2AAD200434d69970AC483BD08B64F ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::GetTemperature(deviceNumber, o_stepReturn2_t1);
            errLabel_14A2AAD200434d69970AC483BD08B64F : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_GetTemperatureState")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_50485390A50647818ED2D3934FBC87E3 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::GetTemperatureState(deviceNumber, o_stepReturn2_t1);
            errLabel_50485390A50647818ED2D3934FBC87E3 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, o_stepReturn2_t1, Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_SendFirmwareCommand")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("command"), command);
            HSLJsonLib::GetStringProperty(objJSONFromServer, Translate("parameter"), parameter);
            onerror goto errLabel_84EE5E4228B140f599748D1271CBB0F3 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::SendFirmwareCommand(deviceNumber, command, parameter);
            errLabel_84EE5E4228B140f599748D1271CBB0F3 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_SetPlateLock")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("plateLock"), plateLock);
            onerror goto errLabel_0B4D6E9CB5BE4050BA49D894F0685FF4 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::SetPlateLock(deviceNumber, plateLock);
            errLabel_0B4D6E9CB5BE4050BA49D894F0685FF4 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_SetShakerParameter")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("shakingDirection"), shakingDirection);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("shakingAccRamp"), shakingAccRamp);
            onerror goto errLabel_451FDB1A50FF4e028560DB4C34C125F1 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            HSLHamHeaterShaker::SetShakerParameter(deviceNumber, shakingDirection, shakingAccRamp);
            errLabel_451FDB1A50FF4e028560DB4C34C125F1 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_SetSimulation")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("simulate"), simulate);
            onerror goto errLabel_B1644184A5B84b0aBDBB58353FF442D0 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            HSLHamHeaterShaker::SetSimulation(simulate);
            errLabel_B1644184A5B84b0aBDBB58353FF442D0 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_SetTempParameter")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("startTimeout"), startTimeout);
            HSLJsonLib::GetFloatProperty(objJSONFromServer, Translate("toleranceRange"), toleranceRange);
            HSLJsonLib::GetFloatProperty(objJSONFromServer, Translate("securityRange"), securityRange);
            onerror goto errLabel_9BC45EC7569E460fB8410F0E23AB29AF ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            HSLHamHeaterShaker::SetTempParameter(deviceNumber, startTimeout, toleranceRange, securityRange);
            errLabel_9BC45EC7569E460fB8410F0E23AB29AF : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_SetUSBTrace")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("trace"), intTrace);
            onerror goto errLabel_FE6D15E135D24fd7A06908E89474B650 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            HSLHamHeaterShaker::SetUSBTrace(intTrace);
            errLabel_FE6D15E135D24fd7A06908E89474B650 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_StartAllShaker")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("shakingSpeed"), shakingSpeed);
            onerror goto errLabel_02BDC1BFC12F4fafA3202E93EF422C02 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::StartAllShaker(shakingSpeed);
            errLabel_02BDC1BFC12F4fafA3202E93EF422C02 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_StartAllShakerTimed")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("shakingSpeed"), shakingSpeed);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("shakingTime"), shakingTime);
            onerror goto errLabel_90F21CFF24BE45c09A6A7000C5D99043 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::StartAllShakerTimed(shakingSpeed, shakingTime);
            errLabel_90F21CFF24BE45c09A6A7000C5D99043 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_StartShaker")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("shakingSpeed"), shakingSpeed);
            onerror goto errLabel_264F4A7DEA214bd38D410C3AE5CAF482 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::StartShaker(dispenseMode, shakingSpeed);
            errLabel_264F4A7DEA214bd38D410C3AE5CAF482 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_StartShakerTimed")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("shakingSpeed"), shakingSpeed);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("shakingTime"), shakingTime);
            onerror goto errLabel_29447729262E4e0f8B347F6640716D96 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::StartShakerTimed(deviceNumber, shakingSpeed, shakingTime);
            errLabel_29447729262E4e0f8B347F6640716D96 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_StartTempCtrl")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("temperature"), temperature);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("waitForTempReached"), waitForTempReached);
            onerror goto errLabel_764F491C76DA445383E5490AB126ADB4 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::StartTempCtrl(deviceNumber, temperature, waitForTempReached);
            errLabel_764F491C76DA445383E5490AB126ADB4 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_StopAllShaker")
        {
            onerror goto errLabel_9B15E9F5E4BF4c8aB941EFAA3E5E122D ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::StopAllShaker();
            errLabel_9B15E9F5E4BF4c8aB941EFAA3E5E122D : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_StopShaker")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_72372634E1DD46ff8400C9F993FCEFB9 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::StopAllShaker();
            errLabel_72372634E1DD46ff8400C9F993FCEFB9 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_StopTempCtrl")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_B5957B02990845739642D8C604B0B582 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::StopTempCtrl(deviceNumber);
            errLabel_B5957B02990845739642D8C604B0B582 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_Terminate")
        {
            onerror goto errLabel_919FCF7F89804c398972DAFE2605D286 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            HSLHamHeaterShaker::Terminate();
            errLabel_919FCF7F89804c398972DAFE2605D286 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_WaitForShaker")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_ED2BDC2CA5D245ccB96A6EDA80EBF4F6 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::WaitForShaker(deviceNumber);
            errLabel_ED2BDC2CA5D245ccB96A6EDA80EBF4F6 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }


        if (commandFromServer == "HHS_WaitForTempCtrl")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            onerror goto errLabel_088C7630997A4749A400740DA66CBA0C ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            o_stepReturn1_t1 = HSLHamHeaterShaker::WaitForTempCtrl(deviceNumber);
            errLabel_088C7630997A4749A400740DA66CBA0C : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }




        if (commandFromServer == "HxFanSet")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("deviceNumber"), deviceNumber);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("persistant"), persistant);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("simulate"), simulate);
            JSON_GetFloatValue(Translate("fanSpeed"), fanSpeed);
            onerror goto errLabel_AA4197CCBE624255B3C96A32C1894C99 ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            if (simulate == 0)
            {
                {
                    HxFan.Simulate("13409ed4_ce79_4ef9_89deb34df8b6dd6a"); }
            }
            else
            {
                {
                    HxFan.Simulate("be3ae73e_7395_494a_9aed80ff221436dc"); }
            }
            {
                HxFan.SetComPort("ffdf7428_8946_4751_8ec8a7e00f208208"); }
            if (persistant == 0)
            {
                {
                    HxFan.SetContinuousMode("d081b2a8_b3ef_4a06_9d8d4d8c6cd1dd39"); }
            }
            else
            {
                {
                    HxFan.SetContinuousMode("4914f72b_ecb0_4ab4_b458a744727e1642"); }
            }
            if (fanSpeed == 0)
            {
                {
                    HxFan.SetFanOff("cef636fc_366e_46f7_9a8e1e25f716fa31"); }
            }
            else
            {
                {
                    HxFan.SetFanSpeed("f2bbd127_49ad_44c1_aa03eba6244b4cfc"); }
            }
            {
                HxFan.CloseComPort("162f7d41_f11e_4261_8602596bf1b6e888"); }
            errLabel_AA4197CCBE624255B3C96A32C1894C99 : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }




        if (commandFromServer == "CORE96WashEmpty")
        {
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("refillAfterEmpty"), refillAfterEmpty);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("chamber1WashLiquid"), chamber1WashLiquid);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("chamber1LiquidChange"), chamber1LiquidChange);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("chamber2WashLiquid"), chamber2WashLiquid);
            HSLJsonLib::GetIntegerProperty(objJSONFromServer, Translate("chamber2LiquidChange"), chamber2LiquidChange);
            onerror goto errLabel_EE8804FCDC214a06935DD0F4830020DB ;
            err.Clear();
            o_stepReturn1_t1 = 0;
            {
                variable arrRetValues[];
                arrRetValues = ML_STAR._19AC7FF8_2C7A_4555_AE3B_3A8CB9466EF3("f4a1383e_67d1_4f19_92f3a5518acddda4"); }
            errLabel_EE8804FCDC214a06935DD0F4830020DB : {}
            onerror goto 0;
            if (err.GetId() != 0)   
            {
                o_stepReturn1_t1 = 1;
            }   
            SendHHSReturnToServer(commandFromServer, o_stepReturn1_t1, Translate(""), Translate(""), Translate(""), id);
        }



    }
}
"""
def gen_oem_hsl():
    with open(target_name, 'w+') as f:
        for c in prefix:
            if c not in '':
                f.write(c)

if __name__ == '__main__':
    gen_oem_hsl()