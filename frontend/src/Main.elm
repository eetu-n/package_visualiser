module Main exposing (main)

import Browser
import Html exposing (Html, div, text, ul, li, span, h5, h4)
import Html.Attributes exposing (id, class)
import Html.Events exposing (onClick)
import Http
import Json.Decode exposing (Decoder, field, string, list, map, map3)
import ScrollTo

main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }

type alias Model = 
    { package_list: (List MultiPackage)
    , package: Maybe SinglePackage
    , scrollTo: ScrollTo.State
    }

init : () -> (Model, Cmd Msg)
init _ =
    ( { package_list = [], package = Nothing, scrollTo = ScrollTo.init}
    , Http.get
        { url = "https://api.pacvis.eetu.dev/package_list"
        , expect = Http.expectJson GotPackageList packageListDecoder
        }
    )

type Msg
    = GotPackageList (Result Http.Error (List MultiPackage))
    | GotPackage (Result Http.Error SinglePackage)
    | ScrollToMsg ScrollTo.Msg
    | ScrollToId String
    | ExpandPackage String
    | CollapsePackage

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        GotPackageList result ->
            case result of
                Ok pkg_list ->
                    ({ package_list = pkg_list, package = model.package, scrollTo = model.scrollTo} , Cmd.none)

                Err _ ->
                    (model, Cmd.none)
        
        GotPackage result ->
            case result of
                Ok pkg ->
                    ({ package_list = model.package_list, package = Just pkg, scrollTo = model.scrollTo}, Cmd.none)
                
                Err _ ->
                    (model, Cmd.none)

        
        ScrollToMsg scrollToMsg ->
            let
                ( scrollToModel, scrollToCmds ) =
                    ScrollTo.update
                        scrollToMsg
                        model.scrollTo
            in
            ( { model | scrollTo = scrollToModel }
            , Cmd.map ScrollToMsg scrollToCmds
            )

        ScrollToId id ->
            ( model
            , Cmd.map ScrollToMsg <|
                ScrollTo.scrollTo id
            )
        
        ExpandPackage name ->
            ( model
            , getPackage name
            )
        
        CollapsePackage ->
            ( { 
                package_list  = model.package_list
                , package       = Nothing
                , scrollTo      = model.scrollTo
                }
            , Cmd.none
            )

subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.map ScrollToMsg <|
        ScrollTo.subscriptions model.scrollTo

type alias MultiPackage = { name: String }

type alias SinglePackage =
    { name: String
    , depends: List MultiPackage
    , rdepends: List MultiPackage
    }

listItem : Model -> MultiPackage -> Html Msg
listItem model pkg =
    case model.package of
        Just modelPackage ->
            if modelPackage.name /= pkg.name then
                collapsedPackage pkg
            else
                expandedPackage modelPackage

        Nothing ->
            collapsedPackage pkg



collapsedPackage : MultiPackage -> Html Msg
collapsedPackage pkg = 
    li
        [ id pkg.name
        , class "package"
        , onClick  (ExpandPackage pkg.name)
        ] 
        [ h4 [] 
            [ text pkg.name 
            , span 
                [ onClick (ExpandPackage pkg.name)
                , class "material-icons md-18"
                ]
                [ text "expand_more"]
            ]
        ]

expandedPackage : SinglePackage -> Html Msg
expandedPackage pkg =
    li
        [ id pkg.name
        , class "package"
        ] 
        [ h4
            []
            [ text pkg.name
            , span
                [ class "material-icons md-18"
                , onClick CollapsePackage
                ]
                [text "expand_less"]
            ]
        , div[]
            [ h5[][text "Depends:"]
            , ul[](List.map subListItem pkg.depends)
            ]

        , div[]
            [ h5[][text "RDepends:"]
            , ul[] (List.map subListItem pkg.rdepends)
            ]
        ]

subListItem : MultiPackage -> Html Msg
subListItem pkg =
    li [class "sublist_package"] 
        [ text pkg.name
        , span
            [ onClick (ScrollToId pkg.name)
            , class "material-icons md-18"
            ]
            [ text "search" ]
        ]


getPackage : String -> Cmd Msg
getPackage package_name =
    Http.get
        { url = "https://api.pacvis.eetu.dev/package/" ++ package_name
        , expect = Http.expectJson GotPackage singlePackageDecoder
        }


packageListDecoder : Decoder (List MultiPackage)
packageListDecoder = 
    field "package_list" multiPackageDecoder

multiPackageDecoder : Decoder (List MultiPackage)
multiPackageDecoder =
    list (map MultiPackage (field "name" string))

singlePackageDecoder : Decoder SinglePackage
singlePackageDecoder =
    map3 SinglePackage
        (field "name" string)
        (field "depends" multiPackageDecoder)
        (field "rdepends" multiPackageDecoder)

view : Model -> Html Msg
view model =
    div []
        [ ul []
            (List.map (listItem model) model.package_list)
        ]